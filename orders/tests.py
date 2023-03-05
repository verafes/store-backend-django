import json
import uuid
from datetime import datetime

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from customers.models import *
from orders.models import Order, OrderProduct
from products.models import Product, Brand
from products.tests import InitProductData


class CartTestCase(APITestCase):
    def test_update_cart(self):
        InitProductData()
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)
        url = reverse('update_cart')
        request_data = {
            "token": customer_token,
            "product_id": 1,
            "quantity": 1
        }
        data = {
            "status": True,
            "cart_items_count": 1
        }
        response = self.client.post(url, data=request_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)


    def test_update_cart_invalid_token(self):
        # create a new customer
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)
        url = reverse('update_cart')
        request_data = {
            "token": "d09c03be-9015-458c-b2c8-d50e43e36a3b",
            "product_id": 1,
            "quantity": 1
        }
        data = {
            "status": False,
            "error": "Customer does not exist"
        }
        response = self.client.post(url, data=request_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), data)


    def test_get_products_in_cart(self):
        # create a new customer
        customer_token = str(uuid.uuid4())
        customer = Customer.objects.create(token=customer_token)
        brand = Brand.objects.create(title='test brand')
        # create a new product for the customer
        product = Product.objects.create(
            title="Test Product",
            price=100,
            old_price=110,
            quantity=5,
            brand=brand,
            description="test description",
        )

        # create a new order for the customer
        order = Order.objects.create(customer=customer)

        # create a new order-product relation
        order_product = OrderProduct.objects.create(
            order=order,
            product=product,
            price=product.price,
            quantity=2
        )

        data = [
            {
                'id': 1,
                'price': '100.00',
                'quantity': 2,
                'product': 1,
                'order': 1,
            },
        ]

        url = reverse('list_products_in_cart', kwargs={'token': customer.token})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

        self.assertEqual(response.data[0]['price'], '100.00')
        self.assertEqual(response.data[0]['quantity'], 2)
        self.assertEqual(response.data[0]['order'], 1)
        self.assertEqual(response.data[0]['product'], 1)


    def test_order_finalize(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

        customer_token = str(uuid.uuid4())
        # Customer.objects.create(token=customer_token, user=self.user)
        customer = Customer.objects.create(
            email='customer@test.com',
            first_name='John',
            last_name='Doe',
            phone='+1234567890',
            token='1234567890'
        )
        address = CustomerAddress.objects.create(
            customer=customer,
            country='USA',
            city='New York',
            post_code='10001',
            address='123 Main St.'
        )
        order = Order.objects.create(
            customer=customer,
            customer_shipping_address=address,
            time_checkout=datetime.now()
        )

        url = reverse('finalize_order')
        data = {
            'token': customer_token,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@test.com',
            'phone': '1234567890',
            'country': 'USA',
            'city': 'New York',
            'post_code': '10001',
            'address': '123 Main St'
        }
        self.client.force_login(self.user)
        response = self.client.put(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.get(pk=order.pk).is_ordered, True)
        self.assertEqual(Customer.objects.get(pk=customer.pk).first_name, 'John')
        self.assertEqual(CustomerAddress.objects.get(pk=address.pk).city, 'New York')

        # test_customer_my_orders -> Fail with error:  line 143, in test_order_finalize
        #     self.assertEqual(response.status_code, status.HTTP_200_OK)
        # AssertionError: 405 != 200
