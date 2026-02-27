from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import response, status
from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import Category, Product

User = get_user_model()


class ProductModelTest(TestCase):
    """Unit tests for Product model properties."""

    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product  = Product.objects.create(
            sku='SKU-001', name='Wireless Mouse',
            category=self.category,
            unit_cost=Decimal('15.00'),
            unit_price=Decimal('29.99'),
            stock=45, reorder_level=20
        )

    def test_inventory_value(self):
        """inventory_value = stock x unit_cost"""
        self.assertEqual(self.product.inventory_value, Decimal('675.00'))

    def test_stock_status_ok(self):
        """Stock well above reorder level should be ok."""
        self.assertEqual(self.product.stock_status, 'ok')

    def test_stock_status_warning(self):
        """Stock within 1.5x reorder level should be warning."""
        self.product.stock = 25  # reorder=20, 1.5x=30 → warning
        self.assertEqual(self.product.stock_status, 'warning')

    def test_stock_status_critical(self):
        """Stock at or below reorder level should be critical."""
        self.product.stock = 20
        self.assertEqual(self.product.stock_status, 'critical')

    def test_soft_delete(self):
        """Deleted product should have is_active=False not be removed."""
        self.product.is_active = False
        self.product.save()
        self.assertFalse(Product.objects.filter(is_active=True, sku='SKU-001').exists())
        self.assertTrue(Product.objects.filter(is_active=False, sku='SKU-001').exists())


class ProductAPITest(APITestCase):
    """Integration tests for the products endpoint."""

    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin', email='admin@test.com',
            password='testpass123', role='admin'
        )
        self.staff = User.objects.create_user(
            username='staff', email='staff@test.com',
            password='testpass123', role='staff'
        )
        self.category = Category.objects.create(name='Electronics')

    def _login(self, email, password):
        response = self.client.post('/api/auth/login/', {
            'email': email, 'password': password
        }, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_admin_can_create_product(self):
        """Admin should be able to create a product."""
        self._login('admin@test.com', 'testpass123')
        response = self.client.post('/api/products/', {
            'sku': 'SKU-001', 'name': 'Wireless Mouse',
            'category': self.category.id,
            'unit_cost': '15.00', 'unit_price': '29.99',
            'reorder_level': 20
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_staff_cannot_create_product(self):
        """Staff should not be able to create a product."""
        self._login('staff@test.com', 'testpass123')
        response = self.client.post('/api/products/', {
            'sku': 'SKU-002', 'name': 'Keyboard',
            'category': self.category.id,
            'unit_cost': '45.00', 'unit_price': '129.99',
            'reorder_level': 15
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_list_products(self):
        """Staff should be able to list products."""
        self._login('staff@test.com', 'testpass123')
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_soft_delete_via_api(self):
        """Deleting a product via API should soft delete it."""
        self._login('admin@test.com', 'testpass123')
        response = self.client.post('/api/products/', {
        'sku': 'SKU-003', 'name': 'Monitor',
        'category': self.category.id,
        'unit_cost': '180.00', 'unit_price': '349.99',
        'reorder_level': 15
        }, format='json')
        product_id = response.data['id']
        self.client.delete(f'/api/products/{product_id}/')
        from inventory.models import Product
        self.assertFalse(Product.objects.filter(is_active=True, sku='SKU-003').exists())

        