from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display   = ['reference', 'type', 'product', 'quantity',
                      'unit_cost', 'unit_price', 'status', 'created_by', 'created_at']
    list_filter    = ['type', 'status', 'created_at']
    search_fields  = ['reference', 'product__name', 'created_by__email']
    ordering       = ['-created_at']
    readonly_fields = ['reference', 'created_at', 'created_by']