import uuid

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, force_authenticate
from rest_framework import status, request
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from customers.models import Customer
from .models import *
from .serializers import ProductSerializer
import unittest
# Show full diff in unittest
unittest.util._MAX_LENGTH=2000

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


class InitOneProductData:
    def __init__(self):
        brand = Brand.objects.create(title='test brand')
        product = Product.objects.create(
            title= 'test brand 1',
            price=100,
            old_price=110,
            quantity=5,
            brand=brand,
            description="test description",
        )
        review = ProductReview.objects.create(
            review='review for the best item',
            fullname='cool',
            product=product
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


    '''title filter'''
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


    '''price filter'''
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


    '''old price filter'''
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


    '''quantity filter'''
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


    '''brand title filter'''
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


    '''brand id filter'''
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


    '''list all drands'''
    def test_product_list_all_brand(self):
        url = reverse('brands_list')
        InitProductData()
        data = [
            {
                'id': 1,
                'title': 'test brand'
            },
        ]
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)


    '''get product by ID'''
    def test_get_product_by_id(self):
        self.pk = 1
        url = reverse('product_by_id', args=[self.pk])
        InitOneProductData()
        data = {
                'id': 1,
                'title': 'test brand 1',
                'price': '100.00',
                'old_price': '110.00',
                'description': 'test description',
                'quantity': 5,
                'photo': None,
                'brand': {
                    'id': 1,
                    'title': 'test brand',
                },
                'reviews': [
                {
                    'id': 1,
                    'review': 'review for the best item',
                    'fullname': 'cool',
                    'product': 1
                }
            ]
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)


    '''list all dcategories'''
    def test_all_categories(self):
        url = reverse('categories_list')

        for i in range(1, 3):
            Category.objects.create(
                id=i,
                title=f'test category {i}',
                is_active=True
            )
        InitProductData()
        data = [
            {
                'id': 1,
                'title': 'test category 1',
                "is_active": True,
            },
            {
                "id": 2,
                "title": "test category 2",
                "is_active": True
            }
        ]
        response = self.client.get(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)


    '''get products in certain category by ID'''
    def test_get_products_in_category_products(self):
        # request_data = Category.objects.filter(is_active=True)
        category = Category.objects.create(title='Test category', is_active=True)
        brand = Brand.objects.create(title='Test brand')
        for i in range(1, 3):
            product = Product.objects.create(
                title=f"Test product {i}",
                price=100,
                old_price=110,
                quantity=5,
                brand=brand,
                description="test description",
            )
            ProductCategory.objects.create(product=product, category=category)
        url = reverse('products_list_by_category', args=[1])
        data = {
            'id': 1,
            'title': 'Test category',
            'category_products': [
                {
                    "product_id": 1,
                    "product_title": "Test product 1"
                },
                {
                    "product_id": 2,
                    "product_title": "Test product 2"
                }
            ]
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Response data: {response.data}")
        self.assertEqual(response.data, data)


    '''add a new product'''
    def test_add_product(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpass')
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)

        brand = Brand.objects.create(title='test brand')
        InitProductData()
        request_data = {
                "title": "New product",
                "price": 50,
                "old_price": 60,
                "quantity": 10,
                "description": "Test description",
                "brand": brand.id
            }
        url = reverse('create_product')
        data = {
            'id': 11,
            'title': 'New product',
            'price': '50.00',
            'old_price': '60.00',
            'description': 'Test description',
            'quantity': 10,
            'photo': None,
            'brand': None,
            'reviews': []
        }
        self.client.force_login(user)
        force_authenticate(request, user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.post(url, data=request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, f"Response data: {response.data}")
        self.assertEqual(response.data, data)


    '''update a product'''
    def test_update_product(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpass')
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)

        InitProductData()
        request_data = {
            "price": 80,
            "old_price": 100,
        }
        url = reverse('product_update', args=[1])

        data = {
            'id': 1,
            'title': 'test brand 1',
            'price': '80.00',
            'old_price': '100.00',
            'description': 'test description',
            'quantity': 5,
            'photo': None,
            'brand': {'id': 1, 'title': 'test brand'},
            'reviews': []
        }
        self.client.force_login(user)
        force_authenticate(request, user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.patch(url, data=request_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Response data: {response.data}")
        self.assertEqual(response.data, data)


    '''delete a product'''
    def test_update_product(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpass')
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)

        InitProductData()

        url = reverse('product_delete', args=[1])

        self.client.force_login(user)
        force_authenticate(request, user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, f"Response data: {response.data}")
