from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Supplier, Customer

User = get_user_model()


class SupplierAPITest(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin', email='admin@test.com',
            password='testpass123', role='admin'
        )
        self.staff = User.objects.create_user(
            username='staff', email='staff@test.com',
            password='testpass123', role='staff'
        )

    def _login(self, email, password):
        response = self.client.post('/api/auth/login/', {
            'email': email, 'password': password
        }, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_admin_can_create_supplier(self):
        """Admin should be able to create a supplier."""
        self._login('admin@test.com', 'testpass123')
        response = self.client.post('/api/suppliers/', {
            'name': 'TechSupply Co',
            'email': 'contact@techsupply.com',
            'phone': '123456789'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_staff_can_create_supplier(self):
        """Staff should also be able to create a supplier."""
        self._login('staff@test.com', 'testpass123')
        response = self.client.post('/api/suppliers/', {
            'name': 'GlobalParts Ltd',
            'email': 'sales@globalparts.com',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_suppliers(self):
        """Should return a list of active suppliers."""
        self._login('staff@test.com', 'testpass123')
        Supplier.objects.create(name='Supplier A')
        Supplier.objects.create(name='Supplier B')
        response = self.client.get('/api/suppliers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 2)

    def test_staff_cannot_delete_supplier(self):
        """Staff should not be able to delete a supplier."""
        self._login('admin@test.com', 'testpass123')
        response = self.client.post('/api/suppliers/', {
            'name': 'To Delete'
        }, format='json')
        supplier_id = response.data['id']
        self._login('staff@test.com', 'testpass123')
        response = self.client.delete(f'/api/suppliers/{supplier_id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_supplier(self):
        """Admin should be able to delete a supplier."""
        self._login('admin@test.com', 'testpass123')
        response = self.client.post('/api/suppliers/', {
            'name': 'To Delete'
        }, format='json')
        supplier_id = response.data['id']
        response = self.client.delete(f'/api/suppliers/{supplier_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CustomerAPITest(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin', email='admin@test.com',
            password='testpass123', role='admin'
        )

    def _login(self, email, password):
        response = self.client.post('/api/auth/login/', {
            'email': email, 'password': password
        }, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_create_customer(self):
        """Admin should be able to create a customer."""
        self._login('admin@test.com', 'testpass123')
        response = self.client.post('/api/customers/', {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '111222333'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_customers(self):
        """Should return a list of customers."""
        self._login('admin@test.com', 'testpass123')
        Customer.objects.create(name='Customer A')
        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)