from django.urls import path
from .views import *

urlpatterns = [
    path('all/', OrderList.as_view(), name='all_orders'),
    path('cart/update/', UpdateCart.as_view(), name='update_cart'),
    path('cart/list/<slug:token>/', CartList.as_view(), name='list_products_in_cart'),
    path('finalize/', OrderFinalize.as_view(),  name='finalize_order')
]