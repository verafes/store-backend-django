from django.http.response import HttpResponse
from requests import Response
from rest_framework import generics, status, request
from rest_framework.views import APIView

from orders.models import Order, OrderProduct
from orders.serializers import OrderSerializer
from customers.models import Customer, CustomerAddress
from products.models import Product
import json


'''List of Orders - api/order/all'''
class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = OrderProduct.objects.all()

    def get_queryset(self):
        return Order.objects.filter(is_ordered=True)


'''List of Products in Order - /api/order/get/<product_id>/'''
class OrderProductList(generics.ListAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderSerializer


'''Method to update data in Cart - api/order/cart/update'''
class UpdateCart(APIView):
    http_method = ['post']

    def post(self, *args, **qargs):
        print("METHOD", request.method)
        try:
            # Check if the customer exists
            try:
                customer = Customer.objects.get(token=self.request.data['token'])
            except Customer.DoesNotExist:
                response = {
                    'status': False,
                    'error': 'Customer does not exist'
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            # Check if the product is available
            try:
                product = Product.objects.get(pk=self.request.data['product_id'])
            except Product.DoesNotExist:
                response = {
                    'status': False,
                    'error': 'Product does not exist'
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            # Default to 1 if quantity is not provided
            requested_quantity = self.request.data.get('quantity', 1)
            # Check if the product quantity is enough in inventory
            if product.quantity < requested_quantity:
                response = {
                    'status': False,
                    'error': 'Not enough product quantity available in inventory'
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            # forming Cart
            orders = Order.objects.filter(customer=customer, is_ordered=False).order_by('-id')
            if orders.count() == 0:
                order = Order.objects.create(customer=customer)
            else:
                order = orders[0]
            try:
                product_order = OrderProduct.objects.get(product=product, order=order)
                if self.request.data['quantity'] == 0:
                    product_order.delete()
                else:
                    product_order.price = product.price
                    product_order.quantity = request.data['quantity']
                    product_order.save()
            except OrderProduct.DoesNotExist:
                    OrderProduct.objects.create(
                        order=order,
                        product=product,
                        price=product.price,
                        quantity=self.request.data['quantity']
                        )
            # count items in Cart
            products_in_order = OrderProduct.objects.filter(order=order)
            count_items = 0
            for item in products_in_order:
                count_items += item['quantity']
            response = {
                'status': True,
                'cart_item_count': count_items
            }
            return Response(data=response, status=status.HTTP_200_OK)

        except BaseException as error:
            response = {
                'status': False,
                'message': str(error)
            }

        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
