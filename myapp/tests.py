import json
from django.test import RequestFactory, TestCase
from django.test import Client
from myapp.views import ProductsView


# Tests
class TestProductsView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_all_products(self):
        view = ProductsView.as_view()
        request = self.factory.get('/products/')
        response = view(request)
        self.assertEqual(response.status_code, 200)  # Assuming 200 is the expected status code for success

    def test_get_products_by_category(self):
        view = ProductsView.as_view()
        request = self.factory.get('/products/4/')  # Change the URL to match your routing
        response = view(request, catID=4)  # Change the catID to a valid category ID
        self.assertEqual(response.status_code, 200)  # Assuming 200 is the expected status code for success
