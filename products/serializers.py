from rest_framework import serializers
from .models import *


'''/api/category/list/'''
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


'''/api/product-category'''
class CategoryProductSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title")
    # category_title = serializers.CharField(source="category.title")

    class Meta:
        model = ProductCategory
        fields = ['product_id', 'product_title']


'''/api/product/get/category/<category_ID> > list of product by category'''
class CategoryProductRetrieveSerializer(serializers.ModelSerializer):
    category_products = CategoryProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'category_products']


'''/api/product/brands/all/ & /api/product/get/brand/<brand_ID>'''
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']


'''to represent brands in ProductList'''
class BrandFields(serializers.RelatedField):

    def to_representation(self, value):
        return {
            'id': value.id,
            'title': value.title,
            }


'''product-reviews'''
class ProductReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductReview
        fields = '__all__'


'''full data for preview product page > api/product/get/id'''
class ProductSerializer(serializers.ModelSerializer):
    brand = BrandFields(many=False, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'old_price', 'description', 'quantity', 'photo', 'brand', "reviews"]


'''product-preview > api/product/all'''
class ProductListSerializer(serializers.ModelSerializer):
    brand = BrandFields(many=False, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'old_price', 'quantity', 'brand', ]

