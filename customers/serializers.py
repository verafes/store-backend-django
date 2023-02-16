from rest_framework import serializers

from .models import Customer, CustomerAddress
from orders.models import Order


'''api/customer/list/'''
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


'''api/address/list/'''
class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = "__all__"


class MyOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
