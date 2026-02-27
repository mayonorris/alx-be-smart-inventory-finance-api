from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from decimal import Decimal
from inventory.models import Category, Product
from partners.models import Supplier
from transactions.models import Transaction
from transactions.services import process_transaction

User = get_user_model()


class ReportsAPITest(APITestCase):

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
        self.supplier = Supplier.objects.create(name='Test Supplier')
        self.product = Product.objects.create(
            sku='SKU-001', name='Wireless Mouse',
            category=self.category,
            unit_cost=Decimal('15.00'),
            unit_price=Decimal('29.99'),
            stock=0, reorder_level=20
        )
        # Add stock and make a sale
        process_transaction({
            'type': Transaction.TransactionType.IN,
            'product': self.product,
            'supplier': self.supplier,
            'quantity': 50,
            'unit_cost': Decimal('15.00'),
            'unit_price': Decimal('0.00'),
            'notes': '', 'status': Transaction.Status.COMPLETED,
        }, self.admin)
        process_transaction({
            'type': Transaction.TransactionType.OUT,
            'product': self.product,
            'supplier': None,
            'quantity': 5,
            'unit_cost': Decimal('15.00'),
            'unit_price': Decimal('29.99'),
            'notes': '', 'status': Transaction.Status.COMPLETED,
        }, self.admin)

    def _login(self, email, password):
        response = self.client.post('/api/auth/login/', {
            'email': email, 'password': password
        }, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_stock_summary_returns_products(self):
        """Stock summary should return a list of products."""
        self._login('admin@test.com', 'testpass123')
        response = self.client.get('/api/reports/stock-summary/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['sku'], 'SKU-001')

    def test_inventory_valuation_correct(self):
        """Inventory value = 45 units x $15 = $675."""
        self._login('admin@test.com', 'testpass123')
        response = self.client.get('/api/reports/inventory-valuation/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total_inventory_value']), 675.0)

    def test_profit_report_correct(self):
        """Revenue = 5 x $29.99 = $149.95, COGS = 5 x $15 = $75, profit = $74.95."""
        self._login('admin@test.com', 'testpass123')
        response = self.client.get('/api/reports/profit/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total_sales_revenue']), 149.95)
        self.assertEqual(float(response.data['total_cogs']), 75.0)
        self.assertEqual(float(response.data['gross_profit']), 74.95)

    def test_profit_report_staff_forbidden(self):
        """Staff should not be able to access profit report."""
        self._login('staff@test.com', 'testpass123')
        response = self.client.get('/api/reports/profit/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_low_stock_empty_when_stock_ok(self):
        """No low stock alerts when all products are above reorder level."""
        self._login('admin@test.com', 'testpass123')
        response = self.client.get('/api/reports/low-stock/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_low_stock_shows_critical_product(self):
        """Product below reorder level should appear in low stock."""
        self.product.stock = 10  # reorder_level=20, so critical
        self.product.save()
        self._login('admin@test.com', 'testpass123')
        response = self.client.get('/api/reports/low-stock/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'critical')

    def test_profit_report_date_filter(self):
        """Profit report should respect date_from and date_to filters."""
        self._login('admin@test.com', 'testpass123')
        response = self.client.get(
            '/api/reports/profit/?date_from=2026-01-01&date_to=2026-12-31'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('gross_profit', response.data)