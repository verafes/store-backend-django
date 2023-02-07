from django.http.response import HttpResponse
from rest_framework import generics

from orders.models import Order, OrderProduct
from orders.serializers import OrderSerializer


'''List of Orders - api/order/all'''
class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(is_ordered=True)


# List of Products in Order - /api/orders/get/products/
class OrderProductList(generics.ListAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderSerializer


def update_cart(request):
    return HttpResponse('Products added to cart')


def cart_list(request):
    return HttpResponse('List of Products in cart')


def checkout(request):
    return HttpResponse('Add shipping address and place order')