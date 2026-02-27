from rest_framework import serializers
from .models import Supplier, Customer


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Supplier
        fields = ['id', 'name', 'email', 'phone', 'address', 'is_active', 'created_at']
        read_only_fields = ['created_at']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Customer
        fields = ['id', 'name', 'email', 'phone', 'address', 'is_active', 'created_at']
        read_only_fields = ['created_at']