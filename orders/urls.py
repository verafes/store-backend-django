from django.urls import path
from .views import *

urlpatterns = [
    path('cart/', update_cart),
    path('cart/list/', cart_list),
    path("list/", order_list),
    path('checkout/', checkout)
]