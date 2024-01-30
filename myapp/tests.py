from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Category, Product, Order
from rest_framework_simplejwt.tokens import RefreshToken

class UserTestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication purposes
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

    def test_register_user(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('register')
        data = {'username': 'newuser', 'password': 'newpassword123', 'email': 'newuser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        """
        Ensure we can login a user and receive a token.
        """
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

class ProductTestCase(APITestCase):
    def setUp(self):
        # Create a test category and product
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', price=10.00, stock=100, category=self.category)

    def test_get_product_list(self):
        """
        Ensure we can retrieve the product list.
        """
        url = reverse('product_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_detail(self):
        """
        Ensure we can retrieve a single product detail.
        """
        url = reverse('product_by_category', kwargs={'catID': self.category.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class OrderTestCase(APITestCase):
    def setUp(self):
        # Create a user and a product for the order
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', price=10.00, stock=100, category=self.category)
        # Create an order
        self.order = Order.objects.create(user=self.user, total_price=100)

        # Obtain a JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_order(self):
        """
        Ensure we can create a new order.
        """
        url = reverse('checkout')
        data = {
            'user': self.user.id,
            'order_details': [
                {'product': self.product.id, 'quantity': 2}
            ],
            'total_price': 20.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)  # Including the order created in setUp

# Add more tests for other views and models as needed
