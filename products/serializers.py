from rest_framework import serializers
from .models import *


'''category/list/'''
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


'''product-category'''
class CategoryProductSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title")
    # category_title = serializers.CharField(source="category.title")

    class Meta:
        model = ProductCategory
        fields = ['product_id', 'product_title', ] #'category_id', 'category_title']


'''product/get/<category_ID>/<products>/'''
class CategoryProductRetrieveSerializer(serializers.ModelSerializer):
    category_products = CategoryProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'category_products']


'''product/brands/all/ & /api/product/get/brand/<brands_ID>'''
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']


'''to represent brands in ProductList'''
class BrandFields(serializers.RelatedField):

    def to_representation(self, value):
        return {
            'id': 'value.id',
            'title': 'value.title'
            }


'''product-reviews'''
class ProductReviewSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(many=False, read_only=True)

    class Meta:
        model = ProductReview
        fields = '__all__'


'''full data for preview product page > api/product/get/id'''
class ProductSerializer(serializers.ModelSerializer):
    brand = BrandFields(many=False, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'old_price', 'description', 'quantity', 'brand', "reviews"]


'''product-preview > api/product/all'''
class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'old_price', 'quantity', 'brand_id']   # no description

