from rest_framework import generics, filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .filters import ProductFilter
from .serializers import *
from .models import *

from django_filters.rest_framework import DjangoFilterBackend
from .paginations import ProductPagination


class CategoryList(generics.ListAPIView):
    '''Endpoint: /api/category/list/ - retrieving a list of categories'''
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(is_active=True)


class CategoryRetrieve(generics.RetrieveAPIView):
    '''Endpoint: /api/category/get/<id> - retrieving a specific category by id'''
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductList(generics.ListAPIView):
    '''Endpoint: api/product/all/ - retrieving a list of products'''
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backend = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('title', 'brand__title',)
    # filterset_fields = ('brand_id', 'price')
    filterset_class = ProductFilter
    pagination_class = ProductPagination


class ProductRetrieve(generics.RetrieveAPIView):
    '''Endpoint: /api/product/get/<product_id>/ - retrieving a product by id'''
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CategoryProductRetrieve(generics.RetrieveAPIView):
    '''Endpoint: /api/product/get/category/<category_ID> > list of products by category'''
    serializer_class = CategoryProductRetrieveSerializer
    queryset = Category.objects.all()


class BrandList(generics.ListAPIView):
    '''Endpoint: api/product/brands/all/ - retrieving a list of brands'''
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class ProductBrandRetrieve(generics.RetrieveAPIView):
    '''Endpoint: /api/product/get/brand/<brands_ID> - retrieving a brand by id'''
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class ProductCreate(generics.CreateAPIView):
    '''Endpoint: api/product/add/ - creating a new product'''
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class ProductRetrieveDestroy(generics.RetrieveUpdateDestroyAPIView):
    '''Endpoint: api/product/rud/<product_id>/ - retrieving, updating, and deleting a product'''
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
