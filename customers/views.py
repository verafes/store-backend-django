from django.http.response import HttpResponse
from rest_framework import generics

from .models import Customer, CustomerAddress
from .serializers import CustomerSerializer


def create_customer(request):
    return HttpResponse('Customer is created')


def create_user(request):
    return HttpResponse('User is registered')


def get_user(request):
    return HttpResponse('Hello user!')


'''List of Customers - api/customer/list'''
class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


'''List of Customer's Addresses - api/customer/address/list'''
class CustomerAddressList(generics.ListAPIView):
    queryset = CustomerAddress.objects.all()
    serializer_class = CustomerSerializer


def my_orders(request):
    return HttpResponse('My orders')


