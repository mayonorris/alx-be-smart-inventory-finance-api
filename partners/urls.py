from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, CustomerViewSet

router = DefaultRouter()
router.register('suppliers', SupplierViewSet, basename='supplier')
router.register('customers', CustomerViewSet, basename='customer')

urlpatterns = [path('', include(router.urls))]