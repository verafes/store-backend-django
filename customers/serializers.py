from rest_framework import serializers

from .models import Customer, CustomerAddress
from orders.models import Order, OrderProduct


'''api/customer/list/'''
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        # fields = "__all__"
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'time_created', 'user_id']


'''api/address/list/'''
class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = "__all__"


class ProductField(serializers.RelatedField):
    def to_representation(self, value):
        return value.title


class MyOrderProductSerializer(serializers.ModelSerializer):
    product = ProductField(many=False, read_only=True)

    class Meta:
        model: OrderProduct
        fields = ['product_id', 'order_id', 'price', 'quantity', 'product']


class MyOrderSerializer(serializers.ModelSerializer):
    products = MyOrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        # fields = '__all__'
        fields = ['id', 'is_ordered', 'time_created', 'time_checkout', 'time_delivery', 'products']

