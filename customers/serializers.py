from rest_framework import serializers

from .models import Customer, CustomerAddress


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


