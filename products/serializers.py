from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    '''/api/category/list/'''
    class Meta:
        model = Category
        fields = '__all__'



class CategoryProductSerializer(serializers.ModelSerializer):
    '''/api/product-category'''
    product_title = serializers.CharField(source="product.title")

    class Meta:
        model = ProductCategory
        fields = ['product_id', 'product_title']


class CategoryProductRetrieveSerializer(serializers.ModelSerializer):
    '''/api/product/get/category/<category_ID> > list of product by category'''
    category_products = CategoryProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'category_products']


class BrandSerializer(serializers.ModelSerializer):
    '''/api/product/brands/all/ & /api/product/get/brand/<brand_ID>'''
    class Meta:
        model = Brand
        fields = ['id', 'title']


class BrandFields(serializers.RelatedField):
    '''to represent brands in ProductList'''
    def to_representation(self, value):
        return {
            'id': value.id,
            'title': value.title,
            }


class ProductReviewSerializer(serializers.ModelSerializer):
    '''product-reviews'''
    class Meta:
        model = ProductReview
        fields = '__all__'

class PhotoField(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.photo.url

class ProductSerializer(serializers.ModelSerializer):
    '''full data for preview product page > api/product/get/id'''
    brand = BrandFields(many=False, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    photo = PhotoField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'old_price', 'description', 'quantity', 'photo', 'brand', "reviews"]


class ProductListSerializer(serializers.ModelSerializer):
    '''product-preview > api/product/all'''
    brand = BrandFields(many=False, read_only=True)
    photo = PhotoField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'old_price', 'quantity', 'brand', ]
