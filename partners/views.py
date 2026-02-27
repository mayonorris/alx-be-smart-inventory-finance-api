from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .models import Supplier, Customer
from .serializers import SupplierSerializer, CustomerSerializer
from accounts.permissions import IsAdminRole, IsStaffOrAdmin


class SupplierViewSet(viewsets.ModelViewSet):
    queryset         = Supplier.objects.filter(is_active=True)
    serializer_class = SupplierSerializer
    filter_backends  = [SearchFilter]
    search_fields    = ['name', 'email']

    def get_permissions(self):
        if self.action in ['destroy']:
            return [IsAdminRole()]
        return [IsStaffOrAdmin()]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset         = Customer.objects.filter(is_active=True)
    serializer_class = CustomerSerializer
    filter_backends  = [SearchFilter]
    search_fields    = ['name', 'email']

    def get_permissions(self):
        if self.action in ['destroy']:
            return [IsAdminRole()]
        return [IsStaffOrAdmin()]