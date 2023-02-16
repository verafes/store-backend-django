from django.urls import path
from .views import *

urlpatterns = [
    path('myorders/', MyOrders.as_view()),
    path('create/', CustomerCreate.as_view()),
    path('list/', CustomerList.as_view()),
    path("address/list/", CustomerAddressList.as_view()),
]