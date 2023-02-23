from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import *

class InitProductData:
    def __init__(self):
        brand = Brand.object.create(title='test brand')
        for i in range(1, 11):
            Product.object.create(
                title=f'test brand {i}',
                price=100,
                old_price=110,
                quantity=5,
                brand=brand,
                description='test description'
            )


class ProductTest(APITestCase):
    def test_product(self):
        url = reverse('list_of_products')
        InitProductData()
        data = {
                "links": {
                    "next": "http://testserver/api/product/all/?page=2",
                    "previous": None,
                    "next_num_page": 2,
                    "previous_num_page": None
                },
                "page": 1,
                "pages": 5,
                "count": 10,
                "result": [
                    {
                        "id": 1,
                        "title": "test brand 1",
                        "price": "100.00",
                        "old_price": "110.00",
                        "quantity": 5,
                        "brand": {
                            "id": 4,
                            "title": "test brand"
                        }
                    },
                    {
                        "id": 2,
                        "title": "test brand 2",
                        "price": "100.00",
                        "old_price": "110.00",
                        "quantity": 5,
                        "brand": {
                            "id": 1,
                            "title": "test brand"
                        }
                    }
                ]
            }
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.asserGreater(Product.objects.count(), 2)
