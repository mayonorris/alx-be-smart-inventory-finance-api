from decimal import Decimal
from django.db import transaction as db_transaction
from rest_framework.exceptions import ValidationError
from .models import Transaction


def _calculate_weighted_avg_cost(current_stock: int, current_cost: Decimal,
                                  new_qty: int, new_cost: Decimal) -> Decimal:
    """
    Weighted Average Cost formula:
        new_avg = (current_stock × current_cost + new_qty × new_cost)
                  ÷ (current_stock + new_qty)
    """
    total_units = current_stock + new_qty
    if total_units == 0:
        return new_cost
    return ((current_stock * current_cost) + (new_qty * new_cost)) / total_units


@db_transaction.atomic
def process_transaction(transaction_data: dict, user) -> Transaction:
    """
    Create a Transaction and update product stock.
    Raises ValidationError for business rule violations.
    """
    product   = transaction_data['product']
    txn_type  = transaction_data['type']
    quantity  = transaction_data['quantity']
    unit_cost = transaction_data.get('unit_cost', product.unit_cost)

    # OUT: prevent negative stock
    if txn_type == Transaction.TransactionType.OUT:
        if quantity > product.stock:
            raise ValidationError(
                f"Insufficient stock. Available: {product.stock}, requested: {quantity}."
            )
        product.stock -= quantity

    # IN: update stock and recalculate weighted average cost
    elif txn_type == Transaction.TransactionType.IN:
        new_avg = _calculate_weighted_avg_cost(
            product.stock, product.unit_cost, quantity, unit_cost
        )
        product.stock     += quantity
        product.unit_cost  = round(new_avg, 2)

    # ADJUST: set stock to absolute value
    elif txn_type == Transaction.TransactionType.ADJUST:
        product.stock = quantity

    product.save()

    txn = Transaction.objects.create(
        **transaction_data,
        created_by=user,
    )
    return txn