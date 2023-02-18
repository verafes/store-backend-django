from django.http.response import HttpResponse
from rest_framework import generics, status

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
def update_cart(request):
    print("METHOD", request.method)
    if request.method == 'POST':
        try:
            request_json = json.loads(request.body)

            customer = Customer.objects.get(token=request_json['token'])
            product = Product.objects.get(pk=request_json['product_id'])
            orders = Order.objects.filter(customer=customer, is_ordered=False).order_by('-id')
            if orders.count() == 0:
                order = Order.objects.create(customer=customer)
            else:
                order = orders[0]
            # if no quantity per request, set default by 1
            if not 'quantity' in request_json:
                request_json['quantity'] = 1
            try:
                product_order = OrderProduct.objects.get(product=product, order=order)
                if request_json['quantity'] == 0:
                    product_order.delete()
                else:
                    product_order.price = product.price
                    product_order.quantity = request_json['quantity']
                    product_order.save()

            except OrderProduct.DoesNotExist:
                OrderProduct.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=request_json['quantity']
                )
            count_products = OrderProduct.objects.filter(order__customer__token=request_json['token']).count()
            response = {
                'status': True,
                'cart_item_count': count_products
            }
            response_status = status.HTTP_200_OK


        except BaseException as error:
            response = {
                'status': False,
                'message': str(error)
            }
            response_status = status.HTTP_400_BAD_REQUEST
    else:
        response = {
            'status': False,
            'message': 'Method not allowed. POST required to update cart'
        }
        response_status = status.HTTP_405_METHOD_NOT_ALLOWED

    return HttpResponse(json.dumps(response), status=response_status)