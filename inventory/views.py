from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from accounts.permissions import IsAdminRole, IsStaffOrAdmin


class CategoryViewSet(viewsets.ModelViewSet):
    queryset           = Category.objects.all()
    serializer_class   = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminRole()]
        return [IsStaffOrAdmin()]


class ProductViewSet(viewsets.ModelViewSet):
    queryset         = Product.objects.select_related('category').filter(is_active=True)
    serializer_class = ProductSerializer
    filter_backends  = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields    = ['name', 'sku', 'description']
    ordering_fields  = ['name', 'stock', 'unit_price', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminRole()]
        return [IsStaffOrAdmin()]

    def perform_destroy(self, instance):
        # Soft delete — never actually removes from DB
        instance.is_active = False
        instance.save()