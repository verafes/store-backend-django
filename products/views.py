from rest_framework import generics
from .serializers import *
from .models import *


'''category/list/'''
class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(is_active=True)


'''category/get/<id>'''
class CategoryRetrieve(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


'''api/product/all/'''
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductPreviewSerializer


'''/api/product/get/<product_id>/'''
class ProductRetrieve(generics.RetrieveAPIView):
    serializer_class = ProductRetrieveSerializer
    queryset = Product.objects.all()


'''/api/product/get/<category_ID>/products/'''
class CategoryProductRetrieve(generics.RetrieveAPIView):
    serializer_class = CategoryProductRetrieveSerializer
    queryset = Category.objects.all()


'''api/product/brands/all/'''
class BrandList(generics.ListAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


'''/api/product/get/<brands_ID> '''
class ProductBrandRetrieve(generics.RetrieveAPIView):
    serializer_class = BrandProductRetrieveSerializer
    queryset = Brand.objects.all()

