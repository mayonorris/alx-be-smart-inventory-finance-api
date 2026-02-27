from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFilter, CharFilter
from rest_framework.filters import OrderingFilter
from .models import Transaction
from .serializers import TransactionSerializer
from .services import process_transaction
from accounts.permissions import IsStaffOrAdmin


class TransactionFilter(FilterSet):
    date_from = DateFilter(field_name='created_at__date', lookup_expr='gte')
    date_to   = DateFilter(field_name='created_at__date', lookup_expr='lte')
    type      = CharFilter(field_name='type')
    product   = CharFilter(field_name='product__id')
    status    = CharFilter(field_name='status')

    class Meta:
        model  = Transaction
        fields = ['type', 'status', 'product', 'date_from', 'date_to']


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.select_related(
        'product', 'supplier', 'customer', 'created_by'
    ).all()
    serializer_class   = TransactionSerializer
    permission_classes = [IsStaffOrAdmin]
    filter_backends    = [DjangoFilterBackend, OrderingFilter]
    filterset_class    = TransactionFilter
    ordering_fields    = ['created_at']
    http_method_names  = ['get', 'post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        txn = process_transaction(serializer.validated_data, request.user)
        out = self.get_serializer(txn)
        return Response(out.data, status=status.HTTP_201_CREATED)