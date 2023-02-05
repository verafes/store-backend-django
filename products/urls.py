from django.urls import path
from .views import *

urlpatterns = [
    path('all/', ProductList.as_view()),
    path('category/list/', CategoryList.as_view()),
    # path('category/get/<int:pk>/', CategoryRetrieve.as_view()),
    path('brands/all/', BrandList.as_view()),
    path('get/<int:pk>/', ProductRetrieve.as_view()),
    path('brands/get/<int:pk>/', ProductBrandRetrieve.as_view()),
    path('category/get/<int:pk>/', CategoryProductRetrieve.as_view())
]