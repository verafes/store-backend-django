from django.urls import path
from .views import *

urlpatterns = [
    path('myorders/', MyOrders.as_view(), name='my_orders'),
    path('create/', CustomerCreate.as_view(), name='customer_create'),
    path('list/', CustomerList.as_view(), name='customers_list'),
    path('address/list/', CustomerAddressList.as_view(), name='address_list'),
]