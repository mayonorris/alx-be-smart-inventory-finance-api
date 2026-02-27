from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthAPITest(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin', email='admin@test.com',
            password='testpass123', role='admin'
        )

    def test_register_new_user(self):
        """Should create a new user with staff role by default."""
        response = self.client.post('/api/auth/register/', {
            'username': 'newuser',
            'email':    'newuser@test.com',
            'password': 'testpass123',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['role'], 'staff')

    def test_register_duplicate_email_fails(self):
        """Should not allow two users with the same email."""
        self.client.post('/api/auth/register/', {
            'username': 'user1',
            'email':    'duplicate@test.com',
            'password': 'testpass123',
        }, format='json')
        response = self.client.post('/api/auth/register/', {
            'username': 'user2',
            'email':    'duplicate@test.com',
            'password': 'testpass123',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_returns_tokens(self):
        """Login should return access and refresh tokens."""
        response = self.client.post('/api/auth/login/', {
            'email':    'admin@test.com',
            'password': 'testpass123',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access',  response.data)
        self.assertIn('refresh', response.data)

    def test_login_token_contains_role(self):
        """Login response should include user object with role."""
        response = self.client.post('/api/auth/login/', {
            'email':    'admin@test.com',
            'password': 'testpass123',
        }, format='json')
        self.assertEqual(response.data['user']['role'], 'admin')

    def test_login_wrong_password_fails(self):
        """Wrong password should return 401."""
        response = self.client.post('/api/auth/login/', {
            'email':    'admin@test.com',
            'password': 'wrongpassword',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_endpoint_returns_current_user(self):
        """Authenticated user should get their own profile from /me/."""
        self.client.post('/api/auth/login/', {
            'email': 'admin@test.com', 'password': 'testpass123'
        }, format='json')
        response = self.client.post('/api/auth/login/', {
            'email': 'admin@test.com', 'password': 'testpass123'
        }, format='json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'admin@test.com')

    def test_me_endpoint_unauthenticated(self):
        """Unauthenticated request to /me/ should return 401."""
        response = self.client.get('/api/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)