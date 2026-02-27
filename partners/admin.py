from django.contrib import admin
from .models import Supplier, Customer


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'phone', 'is_active', 'created_at']
    list_filter   = ['is_active']
    search_fields = ['name', 'email']
    ordering      = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'phone', 'is_active', 'created_at']
    list_filter   = ['is_active']
    search_fields = ['name', 'email']
    ordering      = ['name']