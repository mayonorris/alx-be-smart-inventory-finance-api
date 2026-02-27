from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Transaction
from .serializers import TransactionSerializer
from .services import process_transaction
from accounts.permissions import IsStaffOrAdmin


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.select_related(
        'product', 'supplier', 'customer', 'created_by'
    ).all()
    serializer_class   = TransactionSerializer
    permission_classes = [IsStaffOrAdmin]
    filter_backends    = [DjangoFilterBackend, OrderingFilter]
    filterset_fields   = ['type', 'status', 'product']
    ordering_fields    = ['created_at']
    http_method_names  = ['get', 'post', 'head', 'options']  # No edit/delete

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        txn = process_transaction(serializer.validated_data, request.user)
        out = self.get_serializer(txn)
        return Response(out.data, status=status.HTTP_201_CREATED)