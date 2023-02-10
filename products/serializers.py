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
    category_title = serializers.CharField(source="category.title")

    class Meta:
        model = ProductCategory
        fields = ['product_id', 'product_title', 'category_id', 'category_title']


'''product/get/<category_ID>/products/'''
class CategoryProductRetrieveSerializer(serializers.ModelSerializer):
    category_products = CategoryProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'category_products']


'''product/brands/all/'''
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']


'''product-brand'''
class ProductBrandSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(many=False, read_only=True)

    class Meta:
        model = Product
        #fields = '__all__'
        fields = ['id', 'title', 'price', 'old_price', 'description', 'quantity', 'brand']


'''product/get/<brand_id>/ - retrieve products of the brand'''
class BrandProductRetrieveSerializer(serializers.ModelSerializer):
    brand_products = ProductBrandSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = ['id', 'title', 'brand_products']


'''full data for preview product page'''
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = "__all__"
        fields = ['id', 'title', 'price', 'old_price', 'description', 'quantity', 'brand_id']


'''full data for preview product page '''
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


'''product-preview > api/product/all'''
class ProductPreviewSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        # fields = ['id', 'title', 'price', 'old_price', 'photo', 'brand']


'''/api/product/get/<product_id>/ - full data for preview product page'''
class ProductRetrieve(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


'''product-reviews'''
class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'


'''product-retrieve info'''
class ProductRetrieveSerializer(serializers.ModelSerializer):
    reviews = ProductReviewSerializer(many=True, read_only=True)
    brand = BrandSerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        # fields = ['id', 'title', 'price', 'old_price', 'description', 'quantity', 'brand', 'photo', 'reviews']
