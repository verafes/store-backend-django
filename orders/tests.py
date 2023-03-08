import json
import uuid
from datetime import datetime

from rest_framework import status, request
from rest_framework.test import APITestCase, force_authenticate
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

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
            "token": "test",
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
        # creating a new customer
        customer_token = str(uuid.uuid4())
        customer = Customer.objects.create(token=customer_token)
        # creating a new product for the customer
        brand = Brand.objects.create(title='test brand')
        product = Product.objects.create(
            title="Test Product",
            price=100,
            old_price=110,
            quantity=5,
            brand=brand,
            description="test description",
        )
        # creating a new order for the customer
        order = Order.objects.create(customer=customer)
        # creating a new order-product relation
        OrderProduct.objects.create(
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
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Response data: {response.data}")
        self.assertEqual(response.data, data)

        self.assertEqual(response.data[0]['price'], '100.00')
        self.assertEqual(response.data[0]['quantity'], 2)
        self.assertEqual(response.data[0]['order'], 1)
        self.assertEqual(response.data[0]['product'], 1)


    '''test on Method "POST" not allowed'''
    def test_order_finalize_negative_HTTP_405_METHOD(self):
        # creating a new user
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        # creating a new customer
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token, user=self.user)
        url = reverse('finalize_order')
        self.client.force_login(self.user)
        # post request
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, f"Response data: {response.data}")


    '''finalize order'''
    def test_order_finalize(self):
        # creating a user
        user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        # creating a product
        brand = Brand.objects.create(title='test brand')
        product = Product.objects.create(
            title="Test Product",
            price=100,
            old_price=110,
            quantity=5,
            brand=brand,
            description="test description",
        )
        # creating a customer
        customer_token = str(uuid.uuid4())
        customer = Customer.objects.create(
            email='test@test.com',
            first_name='John',
            last_name='Doe',
            phone='1234567890',
            token=customer_token
        )
        # create a customer address
        address = CustomerAddress.objects.create(
            customer=customer,
            country='USA',
            city='New York',
            post_code='10001',
            address='123 Main St. apt 10'
        )
        # creating an order for the customer
        order = Order.objects.create(customer=customer, is_ordered=False)
        # adding a product to the order
        OrderProduct.objects.create(
            order=order,
            product=product,
            price=product.price,
            quantity=1
        )
        order_data = [
            {
                'id': 1,
                'price': '100.00',
                'quantity': 1,
                'product': 1,
                'order': 1,
            },
        ]
        url = reverse('list_products_in_cart', kwargs={'token': customer.token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Response data: {response.data}")
        self.assertEqual(response.data, order_data)
        print("! order created", response.data[0]['order'])

        order.customer_shipping_address = address
        order.is_ordered = True
        order.time_checkout = datetime.now()
        customer.save()
        order.save()
        print("!order.id:", order.id, "status: ", order.is_ordered, )

        url = reverse('update_cart')
        request_data = {
            "token": customer_token,
            "product_id": 1,
            "quantity": 1
        }
        status_order_data = {
            "status": True,
            "cart_items_count": 1
        }
        response = self.client.post(url, data=request_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("order found for this customer", response.status_code)
        self.assertEqual(json.loads(response.content), status_order_data)
        # creating a JWT token for the user
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        # setting the authentication header
        self.client.force_login(user)
        force_authenticate(request, user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        request_data = {
            "order_id": order.id,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@test.com",
            "post_code": 10001,
            "phone": 1234567890,
            "country": "USA",
            "city": "New York",
            "address": "123 Main St apt 10",
            "token": customer_token
        }
        url = reverse('finalize_order')
        data = {
            'id': 2,
            'time_created': '2023-03-07T04:05:58.693431Z',
            'time_checkout': '2023-03-06T20:05:58.730720Z',
            'time_delivery': '2023-03-07T04:05:58.693431Z',
            'is_ordered': True,
            'customer_id': 1,
            'customer_shipping_address_id': 1
        }
        response = self.client.put(url, data=request_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Response data: {response.data}")
        # self.assertEqual(json.loads(response.content), data, f"Response data: {json.loads(response.content)}")

        self.assertEqual(Order.objects.get(pk=order.pk).is_ordered, True)
        self.assertEqual(Customer.objects.get(pk=customer.pk).first_name, 'John')
        self.assertEqual(CustomerAddress.objects.get(pk=address.pk).city, 'New York')
        self.assertEqual(CustomerAddress.objects.get(pk=address.pk).post_code, '10001')

        self.assertEqual(response.data['id'], data['id'])
        self.assertEqual(response.data['is_ordered'], data['is_ordered'])
        self.assertEqual(response.data['customer'], data['customer_id'])
        self.assertEqual(response.data['customer_shipping_address'], data['customer_shipping_address_id'])

        self.assertEqual(Order.objects.filter(customer=customer, is_ordered=True).count(), 2)
        self.assertEqual(OrderProduct.objects.filter(order=order).count(), 1)
        self.assertEqual(CustomerAddress.objects.filter(customer=customer).count(), 1)
        self.assertEqual(response.data['is_ordered'], True, f"Response data: {response.data}")

        '''test api/order/all/ - all orders for the registered customer'''
        url = reverse('all_orders')
        data = [{
            'id': 1,
            'time_created': '2023-03-07T04:05:58.693431Z',
            'time_checkout': '2023-03-06T20:05:58.730720Z',
            'time_delivery': '2023-03-07T04:05:58.693431Z',
            'is_ordered': True,
            'customer_id': 1,
            'customer_shipping_address_id': 1,
            },
            {
            "id": 2,
            "time_created": "2023-03-06T01:25:11.031667Z",
            "time_checkout": "2023-03-06T01:25:11.031667Z",
            "time_delivery": "2023-03-06T01:25:11.031667Z",
            "is_ordered": True,
            "customer": 7,
            "customer_shipping_address": 1
            }
        ]

        response = self.client.get(url, data=request_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Response data: {response.data}")

        self.assertEqual(response.data[0]['id'], data[0]['id'])
        self.assertEqual(response.data[0]['is_ordered'], data[0]['is_ordered'])
        self.assertEqual(response.data[0]['customer'], data[0]['customer_id'])
        self.assertEqual(response.data[0]['customer_shipping_address'], data[0]['customer_shipping_address_id'])
