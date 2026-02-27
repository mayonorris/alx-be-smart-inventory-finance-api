from decimal import Decimal
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from inventory.models import Product
from transactions.models import Transaction


def get_inventory_valuation():
    products = Product.objects.filter(is_active=True).annotate(
        value=ExpressionWrapper(
            F('stock') * F('unit_cost'),
            output_field=DecimalField(max_digits=16, decimal_places=2)
        )
    )
    total = sum(p.value for p in products) or Decimal('0.00')
    return {
        'total_inventory_value': round(total, 2),
        'products': [
            {
                'id':          p.id,
                'sku':         p.sku,
                'name':        p.name,
                'stock':       p.stock,
                'unit_cost':   p.unit_cost,
                'total_value': round(p.value, 2),
            }
            for p in products
        ]
    }


def get_stock_summary():
    products = Product.objects.select_related('category').filter(is_active=True)
    return [
        {
            'id':            p.id,
            'sku':           p.sku,
            'name':          p.name,
            'category':      p.category.name if p.category else None,
            'stock':         p.stock,
            'reorder_level': p.reorder_level,
            'stock_status':  p.stock_status,
            'unit_cost':     p.unit_cost,
            'unit_price':    p.unit_price,
        }
        for p in products
    ]


def get_low_stock_items():
    products = Product.objects.filter(is_active=True)
    low = []
    for p in products:
        if p.stock_status in ('critical', 'warning'):
            suggested = max(0, (p.reorder_level * 2) - p.stock)
            low.append({
                'id':              p.id,
                'sku':             p.sku,
                'name':            p.name,
                'current_stock':   p.stock,
                'reorder_level':   p.reorder_level,
                'unit_cost':       p.unit_cost,
                'suggested_order': suggested,
                'status':          p.stock_status,
            })
    return sorted(low, key=lambda x: (x['status'] != 'critical', x['current_stock']))


def get_profit_report(date_from=None, date_to=None):
    qs = Transaction.objects.filter(
        type=Transaction.TransactionType.OUT,
        status=Transaction.Status.COMPLETED,
    )
    if date_from:
        qs = qs.filter(created_at__date__gte=date_from)
    if date_to:
        qs = qs.filter(created_at__date__lte=date_to)

    totals = qs.aggregate(
        total_revenue=Sum(
            ExpressionWrapper(F('quantity') * F('unit_price'),
                              output_field=DecimalField(max_digits=16, decimal_places=2))
        ),
        total_cogs=Sum(
            ExpressionWrapper(F('quantity') * F('unit_cost'),
                              output_field=DecimalField(max_digits=16, decimal_places=2))
        ),
    )
    revenue = totals['total_revenue'] or Decimal('0.00')
    cogs    = totals['total_cogs']    or Decimal('0.00')
    profit  = revenue - cogs
    margin  = (profit / revenue * 100) if revenue else Decimal('0.00')

    return {
        'date_from':           str(date_from) if date_from else None,
        'date_to':             str(date_to)   if date_to   else None,
        'total_sales_revenue': round(revenue, 2),
        'total_cogs':          round(cogs,    2),
        'gross_profit':        round(profit,  2),
        'profit_margin':       round(margin,  1),
    }