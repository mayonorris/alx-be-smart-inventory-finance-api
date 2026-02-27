from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at']


class ProductSerializer(serializers.ModelSerializer):
    category_name   = serializers.CharField(source='category.name', read_only=True)
    inventory_value = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    stock_status    = serializers.CharField(read_only=True)

    class Meta:
        model  = Product
        fields = [
            'id', 'sku', 'name', 'description',
            'category', 'category_name',
            'unit_cost', 'unit_price',
            'stock', 'reorder_level',
            'inventory_value', 'stock_status',
            'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['stock', 'inventory_value', 'stock_status', 'created_at', 'updated_at']