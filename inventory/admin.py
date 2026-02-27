from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['name', 'description', 'created_at']
    search_fields = ['name']
    ordering      = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display   = ['sku', 'name', 'category', 'unit_cost', 'unit_price',
                      'stock', 'reorder_level', 'stock_status', 'is_active']
    list_filter    = ['category', 'is_active']
    search_fields  = ['sku', 'name']
    ordering       = ['name']
    readonly_fields = ['stock', 'inventory_value', 'stock_status', 'created_at', 'updated_at']