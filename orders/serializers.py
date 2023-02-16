from rest_framework import serializers
from .models import Order, OrderProduct


'''List of Order - api/order/list/'''
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


'''Products in Order - api/order/list/'''
class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'