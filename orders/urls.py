from django.urls import path
from .views import *

urlpatterns = [
    path("all/", OrderList.as_view(), name="list_of_all_orders"),
    path("get/<int:pk>/", OrderProductList.as_view(), name="get_order"),
    path("cart/update/", UpdateCart.as_view(), name="update_update"),
]