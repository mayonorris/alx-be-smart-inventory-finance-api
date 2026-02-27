from django.urls import path
from .views import StockSummaryView, InventoryValuationView, LowStockView, ProfitReportView

urlpatterns = [
    path('stock-summary/',       StockSummaryView.as_view(),       name='report-stock-summary'),
    path('inventory-valuation/', InventoryValuationView.as_view(), name='report-inventory-valuation'),
    path('low-stock/',           LowStockView.as_view(),           name='report-low-stock'),
    path('profit/',              ProfitReportView.as_view(),       name='report-profit'),
]