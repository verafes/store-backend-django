import json
import uuid
from datetime import datetime
from django.utils import timezone
from datetime import timedelta

from rest_framework import status, request
from rest_framework.test import APITestCase, force_authenticate
from django.urls import reverse

from customers.models import *
from orders.models import Order, OrderProduct
from products.tests import InitProductData, InitUserData


class CartTestCase(APITestCase):
    '''Test: /api/cart/update/'''
    def test_update_cart(self):
        InitProductData()
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)
        url = reverse('update_cart')
        request_data = {
            'token': customer_token,
            'product_id': 1,
            'quantity': 1
        }
        data = {
            'status': True,
            'cart_items_count': 1
        }
        response = self.client.post(url, data=request_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)


    '''Test: /api/cart/update/ - negative - with invalid token'''
    def test_update_cart_invalid_token(self):
        # create a new customer
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)
        url = reverse('update_cart')
        request_data = {
            'token': 'test',
            'product_id': 1,
            'quantity': 1
        }
        data = {
            'status': False,
            'error': 'Customer does not exist'
        }
        response = self.client.post(url, data=request_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), data)

    '''Test: /api/cart/list/<slug:token>/ - List of products in Cart'''
    def test_get_products_in_cart(self):
        # creating a new customer
        customer_token = str(uuid.uuid4())
        customer = Customer.objects.create(token=customer_token)

        # creating a new product for the customer
        init_data = InitProductData()
        product = init_data.product

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
                'product': 10,
                'order': 1,
            },
        ]
        url = reverse('list_products_in_cart', kwargs={'token': customer.token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Response data: {response.data}')
        self.assertEqual(response.data, data)

        self.assertEqual(response.data[0]['price'], data[0]['price'])
        self.assertEqual(response.data[0]['quantity'], data[0]['quantity'])
        self.assertEqual(response.data[0]['order'], data[0]['order'])
        self.assertEqual(response.data[0]['product'], data[0]['product'])


    '''Test: /api/cart/update/ - negative - 'POST' not allowed'''
    def test_order_finalize_negative_HTTP_405_METHOD(self):
        # creating a new user
        user = get_user_model().objects.create_user(username='testuser', password='testpass')
        # creating a new customer
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)
        url = reverse('finalize_order')
        self.client.force_login(user)
        # post request
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                         f'Response data: {response.data}')


    '''Test: /api/cart/finalize/ - finalize order'''
    def test_order_finalize(self):
        # creating a product
        init_data = InitProductData()
        product = init_data.product

        # creating a customer and a user
        init_data = InitUserData()
        user = init_data.user
        token = init_data.token
        customer_token = init_data.customer_token
        customer = init_data.customer

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
        # finalizing the order - 'status is_ordered'
        order.customer_shipping_address = address
        order.is_ordered = True
        order.time_checkout = timezone.now()
        customer.save()
        order.save()

        url = reverse('update_cart')
        request_data = {
            'token': customer_token,
            'product_id': 1,
            'quantity': 1
        }
        status_order_data = {
            'status': True,
            'cart_items_count': 1
        }
        response = self.client.post(url, data=request_data, format='json')
        # order found for this customer
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), status_order_data)

        # authentication
        self.client.force_login(user)
        force_authenticate(request, user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        request_data = {
            'order_id': order.id,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@test.com',
            'post_code': 10001,
            'phone': 1234567890,
            'country': 'USA',
            'city': 'New York',
            'address': '123 Main St apt 10',
            'token': customer_token
        }

        url = reverse('finalize_order')
        data = {
            'id': 2,
            'time_created': datetime.now(),
            'time_checkout': datetime.now(),
            'time_delivery': datetime.now(),
            'is_ordered': True,
            'customer_id': 1,
            'customer_shipping_address_id': 1
        }
        response = self.client.put(url, data=request_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK, f'Response data: {response.data}')

        self.assertEqual(Order.objects.get(pk=order.pk).is_ordered, True)
        self.assertEqual(Customer.objects.get(pk=customer.pk).first_name, 'John')
        self.assertEqual(CustomerAddress.objects.get(pk=address.pk).city, 'New York')
        self.assertEqual(CustomerAddress.objects.get(pk=address.pk).post_code, '10001')

        self.assertEqual(response.data['id'], data['id'])
        self.assertEqual(response.data['is_ordered'], data['is_ordered'])
        self.assertEqual(response.data['customer'], data['customer_id'])
        self.assertEqual(response.data['customer_shipping_address'],
                         data['customer_shipping_address_id'])

        self.assertEqual(Order.objects.filter(customer=customer, is_ordered=True).count(), 2)
        self.assertEqual(OrderProduct.objects.filter(order=order).count(), 1)
        self.assertEqual(CustomerAddress.objects.filter(customer=customer).count(), 1)


    '''test api/order/all/ - all orders for the registered customer'''
    def test_all_finalized_orders(self):
        # creating a product
        init_data = InitProductData()
        product = init_data.product

        # creating a customer and a user
        init_data = InitUserData()
        user = init_data.user
        token = init_data.token
        customer_token = init_data.customer_token
        customer = init_data.customer

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
        # finalizing the order
        order.customer_shipping_address = address
        order.is_ordered = True
        order.time_checkout = timezone.now()
        customer.save()
        order.save()

        url = reverse('update_cart')
        request_data = {
            'token': customer_token,
            'product_id': 1,
            'quantity': 1
        }
        response = self.client.post(url, data=request_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Response data: {json.loads(response.content)}')

        # setting the authentication header
        self.client.force_login(user)
        force_authenticate(request, user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('all_orders')
        data = [{
            'id': 1,
            'time_created': '2023-03-07T04:05:58.693431Z',
            'time_checkout': '2023-03-06T20:05:58.730720Z',
            'time_delivery': '2023-03-07T04:05:58.693431Z',
            'is_ordered': True,
            'customer': 1,
            'customer_shipping_address_id': 1,
            },
        ]
        response = self.client.get(url, data=request_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Response data: {response.data}')
        self.assertEqual(response.data[0]['id'], data[0]['id'])
        self.assertEqual(response.data[0]['is_ordered'], data[0]['is_ordered'])
        self.assertEqual(response.data[0]['customer'], data[0]['customer'])
        self.assertEqual(response.data[0]['customer_shipping_address'],
                         data[0]['customer_shipping_address_id'])
        self.assertEqual(Order.objects.filter(customer=customer, is_ordered=True).count(), 1)
        self.assertEqual(OrderProduct.objects.filter(order=order).count(), 1)
        self.assertEqual(CustomerAddress.objects.filter(customer=customer).count(), 1)


    '''test api/order/finalize/ - no pending orders'''
    def test_order_finalize_no_pending_orders(self):
        init_data = InitUserData()
        url = reverse('finalize_order')
        request_data = {'token': init_data.customer_token}
        response = self.client.put(url, data=request_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f'Response data: {json.loads(response.content)}')


    '''test api/order/finalize/ - no customer'''
    def test_order_finalize_no_customer(self):
        url = reverse('finalize_order')
        request_data = {'token': ''}
        response = self.client.put(url, data=request_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f'Response data: {json.loads(response.content)}')


    '''test api/cart/update/ - no customer'''
    def test_update_cart_no_customer(self):
        url = reverse('update_cart')
        request_data = {'token': ''}
        response = self.client.post(url, data=request_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f'Response data: {json.loads(response.content)}')


    '''test api/order/finalize/ - no product'''
    def test_update_cart_no_product(self):
        init_data = InitUserData()
        url = reverse('update_cart')
        request_data = {
            'token': init_data.customer_token,
            'product_id': 1}
        response = self.client.post(url, data=request_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f'Response data: {json.loads(response.content)}')


    '''test api/order/update/ - 0 quantity in stock'''
    def test_update_cart_zero_quantity(self):
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)
        InitProductData()
        url = reverse('update_cart')
        request_data = {
            'token': customer_token,
            'product_id': 1,
            'quantity': 6}
        response = self.client.post(url, data=request_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f'Response data: {json.loads(response.content)}')


    '''test api/order/finalize/ - delete order older than 2 days'''
    def test_delete_old_order(self):
        # create a customer
        customer_token = str(uuid.uuid4())
        customer = Customer.objects.create(token=customer_token,)
        init_data = InitProductData()
        product = init_data.product
        # create an order that is older than 2 days
        order = Order.objects.create(
            customer=customer,
            is_ordered=False,
        )
        OrderProduct.objects.create(
            order=order,
            product=product,
            price=product.price,
            quantity=2
        )
        order.time_created = timezone.now() - timedelta(days=3)
        order.save()
        data = [
            {
                'id': 1,
                'price': '100.00',
                'quantity': 2,
                'product': 10,
                'order': 1,
            },
        ]
        url = reverse('list_products_in_cart', kwargs={'token': customer.token})
        response = self.client.get(url)
        # assert that the order is not empty and contains the expected data
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Response data: {json.loads(response.content)}')
        self.assertEqual(response.data, data)

        # send a PUT request to finalize the order with the valid token
        url = reverse('finalize_order')
        request_data = {'token': customer_token}

        response = self.client.put(url, data=request_data)
        # assert the response status code and message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f'Response data: {json.loads(response.content)}')
        self.assertEqual(response.data['message'], 'Order was older than 2 days and has been deleted')

        # assert that the order has been deleted
        my_orders = OrderProduct.objects.filter(
            order__customer__token=customer_token,
            order__is_ordered=False
        )
        self.assertEqual(my_orders.count(), 0, f'Response data: {json.loads(response.content)}')
