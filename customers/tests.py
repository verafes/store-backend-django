import json
import uuid
from datetime import datetime

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from customers.models import *
from orders.models import Order


class CustomerTestCase(APITestCase):
    def test_customer_create(self):
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)

        url = reverse('customer_create')
        request_data = {
            'token': customer_token,
        }
        data = {
            'status': True,
            'customer_token': customer_token
        }
        response = self.client.post(url, data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_customer_my_orders(self):
        # create a new customer
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)
        User.objects.create(username='testuser', password='testpass')

        # create a new order for the customer
        order = Order.objects.create(
            customer=Customer.objects.get(token=customer_token),
            is_ordered=True,
            time_created=datetime.now(),
            time_checkout=datetime.now(),
            time_delivery=datetime.now()
        )

        # get the JWT token for the customer
        url = reverse('token_obtain_pair')
        request_data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        response = self.client.post(url, data=request_data, format='json')
        token = response.data['access']

        # set the authorization header to include the JWT token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # GET request to the my_orders endpoint
        response = client.get(url, format='json')

        # check that the response has the order we created
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], order.id)

        self.assertEqual(response.data[0]['is_ordered'], order.is_ordered)
        self.assertEqual(response.data[0]['time_created'], order.time_created.isoformat())
        self.assertEqual(response.data[0]['time_checkout'], order.time_checkout.isoformat())
        self.assertEqual(response.data[0]['time_delivery'], order.time_delivery.isoformat())

        # test_customer_my_orders -> Fail with error: line 52, in test_customer_my_orders
        # token = response.data['access']
        # KeyError: 'access'