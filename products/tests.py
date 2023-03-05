from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import *


class InitProductData:
    def __init__(self):
        brand = Brand.objects.create(title='test brand')
        for i in range(1, 11):
            Product.objects.create(
                title=f"test brand {i}",
                price=100,
                old_price=110,
                quantity=5,
                brand=brand,
                description="test description",
            )


class ProductTestCase(APITestCase):
    def test_product(self):
        url = reverse('list_of_products')
        InitProductData()
        data = {
            'links': {
                'next': 'http://testserver/api/product/all/?page=2',
                'previous': None,
                'next_num_page': 2,
                'previous_num_page': None
            },
            'page': 1,
            'pages': 5,
            'count': 10,
            'result': [
                {
                    'id': 1,
                    'title': 'test brand 1',
                    'price': '100.00',
                    'old_price': '110.00',
                    'quantity': 5,
                    'brand': {
                        'id': 1,
                        'title': 'test brand',
                    }
                },
                {
                    'id': 2,
                    'title': 'test brand 2',
                    'price': '100.00',
                    "old_price": '110.00',
                    'quantity': 5,
                    'brand': {
                        'id': 1,
                        'title': 'test brand',
                    }
                }
            ]
        }
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(Product.objects.count(), 2)
        self.assertEqual(response.data, data)


    '''test on title filter'''
    def test_product_list_title_filter(self):
        url = reverse('list_of_products')
        InitProductData()

        search_title = "test brand 1"
        parameters = dict(
            title=search_title
        )

        response = self.client.get(url, params=parameters)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['title'], search_title)


    '''test on price filter'''
    def test_product_list_price_filter(self):
        url = reverse('list_of_products')
        InitProductData()
        search_price = "{:.2f}".format(100.00)
        parameters = dict(
            price=search_price
        )
        response = self.client.get(url, params=parameters)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['price'], search_price)


    '''test on old price filter'''
    def test_product_list_old_price_filter(self):
        url = reverse('list_of_products')
        InitProductData()
        search_old_price = "{:.2f}".format(110.00)
        parameters = dict(
            old_price=search_old_price
        )
        response = self.client.get(url, params=parameters)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['old_price'], search_old_price)


    '''test on quantity filter'''
    def test_product_list_quantity_filter(self):
        url = reverse('list_of_products')
        InitProductData()
        search_quantity = 5
        parameters = dict(
            quantity=search_quantity
        )
        response = self.client.get(url, params=parameters)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['quantity'], search_quantity)


    '''test on brand title filter'''
    def test_product_list_brand_filter(self):
        url = reverse('list_of_products')
        InitProductData()
        search_brand_title = 'test brand'
        parameters = dict(
            brand=search_brand_title
        )
        response = self.client.get(url, params=parameters)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['brand']['title'], search_brand_title)

    '''test on brand title filter'''

    def test_product_list_brand_id_filter(self):
        url = reverse('list_of_products')
        InitProductData()
        search_brand_id = 1
        parameters = dict(
            brand=search_brand_id
        )
        response = self.client.get(url, params=parameters)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['brand']['id'], search_brand_id)

