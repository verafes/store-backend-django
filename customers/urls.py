from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_customer),   # guest user
    path('list/', CustomerList.as_view()),
    path("registration/", create_user),   # registered user
    path('user/', get_user),
    path('myorders/', my_orders),
    path("address/list/", CustomerAddressList.as_view()),
]