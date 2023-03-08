from django.http.response import HttpResponse
from rest_framework import generics, filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .filters import ProductFilter
from .serializers import *
from .models import *
import json

from django_filters.rest_framework import DjangoFilterBackend
from .paginations import ProductPagination


'''/api/category/list/'''
class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(is_active=True)


'''/api/category/get/<id>'''
class CategoryRetrieve(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


'''api/product/all/'''
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backend = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('title', 'brand__title',)
    # filterset_fields = ('brand_id', 'price')
    filterset_class = ProductFilter
    pagination_class = ProductPagination


'''/api/product/get/<product_id>/'''
class ProductRetrieve(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


'''/api/product/get/category/<category_ID> > list of products by category'''
class CategoryProductRetrieve(generics.RetrieveAPIView):
    serializer_class = CategoryProductRetrieveSerializer
    queryset = Category.objects.all()


'''api/product/brands/all/'''
class BrandList(generics.ListAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


'''/api/product/get/brand/<brands_ID> '''
class ProductBrandRetrieve(generics.RetrieveAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


'''api/product/add/'''
class ProductCreate(generics.CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


'''api/product/rud/<product_id>/'''
class ProductRetrieveDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

