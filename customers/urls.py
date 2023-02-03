from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_customer),   # guest user
    path('list/', list_customers),
    path("registration/", create_user),   # registered user
    path('user/', get_user),
    path('myorders/', my_orders),
    path("address/list/", address_list),
]