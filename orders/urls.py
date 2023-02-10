from django.urls import path
from .views import *

urlpatterns = [
    path('cart/', update_cart),
    path('cart/list/', cart_list),
    # path("orders/list/", OrderProductList.as_view()),
    path("orders/list/", order_list),
    # path("order_product/list/", OrderProductList.as_view()),
    path('checkout/', checkout)
]