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

    # def test_post_product(self):
        # view = ProductsView.as_view()
        # data = {"desc": "Test Product", "price": 10.99, "ctg": "4"}
        # request = self.factory.post('/products/',  _RequestData = json.dumps(data),str = 'application/json')
        # response = view(request)
        # self.assertEqual(response.status_code, 201)  # Assuming 201 is the expected status code for successful creation

    # def test_put_product(self):
    #     # Assuming an existing product ID for update
    #     product_id = 1  # Change to a valid product ID
    #     view = ProductsView.as_view()
    #     data = {'name': 'Updated Product', 'price': 15.99}  # Change as needed
    #     request = self.factory.put(f'/products/{product_id}/', data=json.dumps(data), content_type='application/json')
    #     response = view(request)
    #     self.assertEqual(response.status_code, 200)  # Assuming 200 is the expected status code for success

    # def test_delete_product(self):
    #     # Assuming an existing product ID for deletion
    #     product_id = 1  # Change to a valid product ID
    #     view = ProductsView.as_view()
    #     request = self.factory.delete(f'/products/{product_id}/')
    #     response = view(request)
    #     self.assertEqual(response.status_code, 204)  