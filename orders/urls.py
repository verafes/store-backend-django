from django.urls import path
from .views import *

urlpatterns = [
    path("all/", OrderList.as_view()),
    path("get/<int:pk>/", OrderProductList.as_view()),
    path("cart/update/", update_cart),
]