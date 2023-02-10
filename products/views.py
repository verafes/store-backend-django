from django.http.response import HttpResponse
from rest_framework import generics
from .serializers import *
from .models import *
import json
from django.db.models import Q

'''category/list/'''
class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        # return Category.objects.filter(is_active=True)
        #SQL SELECT * FROM categories WHERE title = "Women's snowboards" AND is_active=True
        return Category.objects.filters(Q(title = "Women's snowboards") | Q(is_active=True))

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


# api/product/add/
class ProductCreate(generics.CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


'''variants with funcs '''
def product_list(request):
    products = Product.objects.all()
    prods_list = []
    for prod in products:
        tmp_prod = {
            'id': prod.id,
            'title': prod.title,
            'price': float(prod.price),
            'old_price': float(prod.old_price),
            'quantity': prod.quantity,
            'brand_id': prod.brand_id,
        }
        prods_list.append(tmp_prod)

    return HttpResponse(json.dumps(prods_list))


def retrieve_product(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        data = {
            'id': product.id,
            'title': product.title,
            'price': float(product.price),
            'old_price': float(product.old_price),
            'quantity': product.quantity,
            'brand_id': product.brand_id,
        }
    except Product.DoesNotExist:
        data = {"error": "Product does not exist"}

    return HttpResponse(json.dumps(data))


def delete_product(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        data = {
            'id': product.id,
            'message': "success",
        }
        product.delete()
    except Product.DoesNotExist:
        data = {"error": "Product does not exist"}

    return HttpResponse(json.dumps(data))



