from django.http.response import HttpResponse
from rest_framework import generics

from orders.models import Order, OrderProduct
from orders.serializers import OrderSerializer


'''List of Orders - api/order/all'''
class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = OrderProduct.objects.all()

    # def get_queryset(self):
    #     return Order.objects.filter(is_ordered=True)


'''List of Products in Order - /api/order/get/<product_id>/'''
class OrderProductList(generics.ListAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderSerializer

