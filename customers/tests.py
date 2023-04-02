import json
import uuid
from datetime import datetime

from rest_framework import status, request
from rest_framework.test import APITestCase, force_authenticate
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from customers.models import *
from orders.models import Order, OrderProduct
from products.tests import InitProductData, InitUserData


class CustomerTestCase(APITestCase):
    '''Test: /api/customer/create/'''
    def test_customer_create(self):
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)
        url = reverse('customer_create')
        request_data = {
            'token': customer_token,
        }
        response = self.client.post(url, data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         f'Response data: {json.loads(response.content)}')
        self.assertEqual(response.data['status'], True)

    '''Test: /api/customer/list/'''
    def test_customer_list_authenticated(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        customer_token = str(uuid.uuid4())
        customer = Customer.objects.create(
            user=user,
            token=customer_token
        )
        AccessToken.for_user(user)
        self.client.force_login(user)
        data = [
            {
                'id': 1,
                'first_name': '',
                'last_name': '',
                'phone': None,
                'email': '',
                'time_created': '2023-02-21T05:38:44.026171Z',
                'user_id': 1
            },
        ]
        response = self.client.get(reverse('customers_list'))
        self.assertEqual(response.status_code, 200,
                         f'Response data: {json.loads(response.content)}')
        self.assertTrue(customer.first_name in str(response.content))
        self.assertEqual(response.data[0]['id'], data[0]['id'])
        self.assertEqual(response.data[0]['user_id'], data[0]['user_id'])


    '''Test: /api/customer/registration/'''
    def test_user_registration(self):
        customer_token = str(uuid.uuid4())
        customer = Customer.objects.create(token=customer_token)
        self.assertIsNotNone(customer.token)
        # Creating a test user
        request_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'testpass',
            'token': customer_token
        }
        url = reverse('create_user')
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         f'Response data: {json.loads(response.content)}')

        # Checking that the user was created
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Customer.objects.filter(user__username='testuser').exists())

        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.id, 1)


    '''test: user is not authuthorized'''
    def test_token_obtain_pair_401_UNAUTHORIZED(self):
        request_data = {
            'username': 'testuser',
            'password': 'testpass',
        }
        data = {
            'detail': 'No active account found with the given credentials'
        }
        url = reverse('token_obtain_pair')
        response = self.client.post(url, data=request_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         f'Response data: {json.loads(response.content)}')
        self.assertNotIn('access', response.data)
        self.assertEqual(json.loads(response.content), data)

    '''Test: api/jwt/auth/ - authentication with JWT token'''
    def test_token_obtain_pair_positive(self):
        InitUserData()
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'testpass',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Response data: {json.loads(response.content)}')
        self.assertIn('access', response.data)


    '''Test: /api/customer/myorders'''
    def test_customer_my_orders(self):
        # creating a customer and a user
        init_user_data = InitUserData()
        user = init_user_data.user
        token = init_user_data.token
        customer_token = init_user_data.customer_token

        # creating a new product, adding to cart
        InitProductData()
        url = reverse('update_cart')
        request_data = {
            'token': customer_token,
            'product_id': 1,
            'quantity': 1}
        response = self.client.post(url, data=request_data, format='json')
        # verifying order is created
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['cart_items_count'], 1)

        # creating a new order for the customer
        order = Order.objects.create(
            customer=Customer.objects.get(token=customer_token),
            is_ordered=True,
            time_created=datetime.now(),
            time_checkout=datetime.now(),
            time_delivery=datetime.now()
        )
        # authorization with JWT token
        self.client.force_login(user)
        force_authenticate(request, user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
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
        data = [
            {
                'id': 1,
                'is_ordered': True,
                'time_created': datetime.now(),
                'time_checkout': datetime.now(),
                'time_delivery': datetime.now(),
                'customer_id': 1,
            }
        ]
        # finalizing order
        url = reverse('finalize_order')
        response = self.client.put(url, data=request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f'Response data: {json.loads(response.content)}')
        self.assertEqual(Order.objects.get(pk=order.pk).is_ordered, True)

        # GET request to the my_orders endpoint
        url = reverse('my_orders')
        response = self.client.get(url, data=request_data, format='json')

        # checking that the response has the order we created ->> test fails : my_orders=[]
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Response data: {json.loads(response.content)}')
        self.assertEqual(response.data[0]['id'], data[0]['id'])
        self.assertEqual(response.data[0]['is_ordered'], data[0]['is_ordered'])


    '''Negative test: /api/customer/myorders with not valid token'''
    def test_customer_my_orders_negative_token_not_valid(self):
        # creating a customer and a user
        init_data = InitUserData()
        user = init_data.user
        token = init_data.customer_token  # not valid
        customer_token = init_data.customer_token

        # creating a new order for the customer
        Order.objects.create(
            customer=Customer.objects.get(token=customer_token),
            is_ordered=True,
            time_created=datetime.now(),
            time_checkout=datetime.now(),
            time_delivery=datetime.now()
        )
        # setting the authorization header to include the JWT token
        self.client.force_login(user)
        force_authenticate(request, user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data = {
            'detail': 'Given token not valid for any token type',
            'code': 'token_not_valid',
            'messages': [
                {
                    'token_class': 'AccessToken',
                    'token_type': 'access',
                    'message': 'Token is invalid or expired'
                }
            ]
        }
        url = reverse('my_orders')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         f'Response data: {json.loads(response.content)}')
        self.assertEqual(json.loads(response.content), data,
                         f'Response data: {json.loads(response.content)}')
