from decimal import Decimal
from django.db import transaction as db_transaction
from rest_framework.exceptions import ValidationError
from .models import Transaction

"""
Transaction service layer.

All stock mutation logic lives here — never directly in views.
This ensures atomic operations and clean separation of concerns.
"""
from decimal import Decimal
from django.db import transaction as db_transaction
from rest_framework.exceptions import ValidationError
from .models import Transaction

def _calculate_weighted_avg_cost(current_stock: int, current_cost: Decimal,
                                  new_qty: int, new_cost: Decimal) -> Decimal:
    """
    Calculate the new weighted average cost after a purchase.

    Formula:
        new_avg = (current_stock × current_cost + new_qty × new_cost)
                  ÷ (current_stock + new_qty)

    Args:
        current_stock: Current quantity in stock.
        current_cost:  Current weighted average unit cost.
        new_qty:       Quantity being purchased.
        new_cost:      Unit cost of the new purchase.

    Returns:
        New weighted average cost as Decimal.
    """
    total_units = current_stock + new_qty
    if total_units == 0:
        return new_cost
    return ((current_stock * current_cost) + (new_qty * new_cost)) / total_units

@db_transaction.atomic
def process_transaction(transaction_data: dict, user) -> Transaction:
    """
    Create a Transaction and update product stock accordingly.

    Business rules enforced:
        - IN:     Increases stock. Recalculates weighted average cost.
        - OUT:    Decreases stock. Raises ValidationError if quantity
                  exceeds available stock (prevents negative inventory).
        - ADJUST: Sets stock to an absolute value for corrections.

    All operations are wrapped in a database transaction — if anything
    fails, the stock update and transaction record are both rolled back.

    Args:
        transaction_data: Validated data dict from TransactionSerializer.
        user:             The authenticated user creating the transaction.

    Returns:
        The created Transaction instance.

    Raises:
        ValidationError: If an OUT transaction exceeds available stock.
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