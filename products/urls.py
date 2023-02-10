from django.urls import path
from .views import *

urlpatterns = [
    path('all/', ProductList.as_view(), name="list_of_products"),
    path('category/list/', CategoryList.as_view()),
    # path('category/get/<int:pk>/', CategoryRetrieve.as_view()),
    path('category/get/<int:pk>/', CategoryProductRetrieve.as_view()),
    path('brands/all/', BrandList.as_view()),
    path('get/<int:pk>/', ProductRetrieve.as_view()),
    path('brands/get/<int:pk>/', ProductBrandRetrieve.as_view()),
    path('goods/', product_list),
    path('good/<int:product_id>/', retrieve_product),
    path('good/delete/<int:product_id>/', delete_product),
    path('add/', ProductCreate.as_view(), name="create_product")
]