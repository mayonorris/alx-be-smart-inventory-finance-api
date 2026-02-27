from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from inventory.models import Category, Product
from partners.models import Supplier
from transactions.models import Transaction
from transactions.services import process_transaction, _calculate_weighted_avg_cost

User = get_user_model()


class WACCalculationTest(TestCase):
    """Unit tests for the weighted average cost formula."""

    def test_basic_wac(self):
        """50 units @ $10 + 50 units @ $20 = avg $15"""
        result = _calculate_weighted_avg_cost(50, Decimal('10.00'), 50, Decimal('20.00'))
        self.assertEqual(result, Decimal('15.00'))

    def test_wac_empty_stock(self):
        """When current stock is 0, new cost becomes the average."""
        result = _calculate_weighted_avg_cost(0, Decimal('0.00'), 10, Decimal('25.00'))
        self.assertEqual(result, Decimal('25.00'))

    def test_wac_same_price(self):
        """Same price should return the same price."""
        result = _calculate_weighted_avg_cost(100, Decimal('15.00'), 50, Decimal('15.00'))
        self.assertEqual(result, Decimal('15.00'))

    def test_wac_weighted_correctly(self):
        """100 units @ $10 + 10 units @ $20 = avg $10.91"""
        result = _calculate_weighted_avg_cost(100, Decimal('10.00'), 10, Decimal('20.00'))
        self.assertAlmostEqual(float(result), 10.909, places=2)


class TransactionAPITest(APITestCase):
    """Integration tests for the transactions endpoint."""

    def setUp(self):
        # Create admin user
        self.admin = User.objects.create_user(
            username='admin', email='admin@test.com',
            password='testpass123', role='admin'
        )
        # Create category, product, supplier
        self.category = Category.objects.create(name='Test Category')
        self.product  = Product.objects.create(
            sku='SKU-TEST', name='Test Product',
            category=self.category,
            unit_cost=Decimal('10.00'),
            unit_price=Decimal('20.00'),
            stock=0, reorder_level=5
        )
        self.supplier = Supplier.objects.create(name='Test Supplier')

        # Get JWT token
        response = self.client.post('/api/auth/login/', {
            'email': 'admin@test.com', 'password': 'testpass123'
        }, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_purchase_increases_stock(self):
        """IN transaction should increase product stock."""
        self.client.post('/api/transactions/', {
            'type': 'IN', 'product': self.product.id,
            'supplier': self.supplier.id,
            'quantity': 50, 'unit_cost': '10.00'
        }, format='json')
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 50)

    def test_purchase_updates_wac(self):
        """Second IN at different price should update weighted average cost."""
        # First purchase: 50 units @ $10
        self.client.post('/api/transactions/', {
            'type': 'IN', 'product': self.product.id,
            'quantity': 50, 'unit_cost': '10.00'
        }, format='json')
        # Second purchase: 50 units @ $20
        self.client.post('/api/transactions/', {
            'type': 'IN', 'product': self.product.id,
            'quantity': 50, 'unit_cost': '20.00'
        }, format='json')
        self.product.refresh_from_db()
        self.assertEqual(self.product.unit_cost, Decimal('15.00'))

    def test_sale_decreases_stock(self):
        """OUT transaction should decrease product stock."""
        # First add stock
        self.client.post('/api/transactions/', {
            'type': 'IN', 'product': self.product.id,
            'quantity': 50, 'unit_cost': '10.00'
        }, format='json')
        # Then sell
        self.client.post('/api/transactions/', {
            'type': 'OUT', 'product': self.product.id,
            'quantity': 5, 'unit_cost': '10.00', 'unit_price': '20.00'
        }, format='json')
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 45)

    def test_sale_prevents_negative_stock(self):
        """OUT transaction exceeding stock should return 400."""
        response = self.client.post('/api/transactions/', {
            'type': 'OUT', 'product': self.product.id,
            'quantity': 999, 'unit_cost': '10.00', 'unit_price': '20.00'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reference_auto_generated(self):
        """Transaction reference should be auto-generated in TXN-XXXX format."""
        response = self.client.post('/api/transactions/', {
            'type': 'IN', 'product': self.product.id,
            'quantity': 10, 'unit_cost': '10.00'
        }, format='json')
        self.assertIn('TXN-', response.data['reference'])

    def test_unauthenticated_request_rejected(self):
        """Request without token should return 401."""
        self.client.credentials()  # remove token
        response = self.client.get('/api/transactions/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)