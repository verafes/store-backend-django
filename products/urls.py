from django.urls import path
from .views import *

urlpatterns = [
    path('all/', ProductList.as_view(), name='list_of_products'),
    path('category/list/', CategoryList.as_view(), name='categories_list'),
    path('category/get/<int:pk>/', CategoryRetrieve.as_view(), name='category_by_id'),
    path('get/category/<int:pk>/', CategoryProductRetrieve.as_view(), name='products_list_by_category'),
    path('brands/all/', BrandList.as_view(), name='brands_list'),
    path('add/', ProductCreate.as_view(), name='create_product'),
    path('rud/<int:pk>/delete/', ProductRetrieveDestroy.as_view(), name='product_delete'),
    path('rud/<int:pk>/', ProductRetrieveDestroy.as_view(), name='product_update'),
    path('brand/<int:pk>/', ProductBrandRetrieve.as_view(), name='brand_by_id'),
    path('get/<int:pk>/', ProductRetrieve.as_view(), name='product_by_id'),
]