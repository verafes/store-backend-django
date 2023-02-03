from django.urls import path
from .views import *

urlpatterns = [
    path('all', product_list),
    path('category/list', category_list),
    path('brands/all', brand_list),
    path('get/<int:id>/', get_product),
    path('brands/get/<int:id>/', get_brand),
    path('category/get/<int:id>/', get_category)
]