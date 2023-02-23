import json
import uuid

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from customers.models import *
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