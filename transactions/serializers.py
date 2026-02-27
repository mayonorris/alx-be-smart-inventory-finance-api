from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    product_name     = serializers.CharField(source='product.name',      read_only=True)
    supplier_name    = serializers.CharField(source='supplier.name',     read_only=True)
    customer_name    = serializers.CharField(source='customer.name',     read_only=True)
    created_by_email = serializers.CharField(source='created_by.email',  read_only=True)
    total_amount     = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model  = Transaction
        fields = [
            'id', 'reference', 'type', 'status',
            'product', 'product_name',
            'supplier', 'supplier_name',
            'customer', 'customer_name',
            'quantity', 'unit_cost', 'unit_price', 'total_amount',
            'notes', 'created_by', 'created_by_email', 'created_at',
        ]
        read_only_fields = ['reference', 'created_by', 'created_at', 'total_amount']