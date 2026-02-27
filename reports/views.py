from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from accounts.permissions import IsStaffOrAdmin, IsAdminRole
from .services import (
    get_inventory_valuation,
    get_stock_summary,
    get_low_stock_items,
    get_profit_report,
)


class DateRangeSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=False, allow_null=True)
    date_to   = serializers.DateField(required=False, allow_null=True)


class StockSummaryView(APIView):
    permission_classes = [IsStaffOrAdmin]

    def get(self, request):
        return Response(get_stock_summary())


class InventoryValuationView(APIView):
    permission_classes = [IsStaffOrAdmin]

    def get(self, request):
        return Response(get_inventory_valuation())


class LowStockView(APIView):
    permission_classes = [IsStaffOrAdmin]

    def get(self, request):
        return Response(get_low_stock_items())


class ProfitReportView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        s = DateRangeSerializer(data=request.query_params)
        s.is_valid(raise_exception=True)
        return Response(get_profit_report(
            date_from=s.validated_data.get('date_from'),
            date_to=s.validated_data.get('date_to'),
        ))