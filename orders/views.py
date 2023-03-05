import datetime

from rest_framework import generics, status, request
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from orders.models import Order, OrderProduct
from orders.serializers import OrderSerializer, OrderProductSerializer
from customers.models import Customer, CustomerAddress
from products.models import Product


'''List of Orders - api/order/all'''
class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(is_ordered=True)


'''List Products in Order - /api/order/get/<product_id>/'''
class OrderProductList(generics.ListAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderSerializer


'''Method to update data in Cart - api/order/cart/update'''
class UpdateCart(APIView):
    http_method = ['post']

    def post(self, *args, **qargs):
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
                    product_order.quantity = self.request.data['quantity']
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
                count_items += item.quantity   # item['quantity']
            response = {
                'status': True,
                'cart_items_count': count_items
            }
            # Update the product quantity in the inventory
            product.quantity = product.quantity - requested_quantity
            product.save()

            return Response(data=response, status=status.HTTP_200_OK)

        except BaseException as error:
            response = {
                'status': False,
                'message': str(error)
            }
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


'''List of Products in Cart - /api/card/list/<token>/'''
class CartList(generics.ListAPIView):
    serializer_class = OrderProductSerializer
    def get_queryset(self):
        try:
            return OrderProduct.objects.filter(
                order__customer__token=self.kwargs['token'],
                order__is_ordered=False
            )
        except BaseException:
            return None


'''api/order/finalize/'''
@permission_classes([AllowAny])
class OrderFinalize(APIView):
    http_method = ['put']

    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(token=self.request.data['token'])
            order = Order.objects.filter(customer=customer, is_ordered=False).order_by('-id').first()

            if order is None:
                return Response({
                    'message': 'No pending order found for this customer'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(order, data=request.data, partial=True)
            serializer.is_valid(raise_exeption=True)
            self.preform_update(serializer)

            customer.first_name = self.request.data.get('first_name', customer.first_name)
            customer.last_name = self.request.get('last_name', customer.last_name)
            customer.email = self.request.data.get('email', customer.email)
            customer.phone = self.request.data.get('phone', customer.phone)
            customer.save()

            # checking if the address is already created in database
            try:
                address = CustomerAddress.objects.get(customer=customer)
                address.country = self.request.data['country']
                address.city = self.request.data['city']
                address.post_code = self.request.data['post_code']
                address.address = self.request.data['address']
                address.save()
            except CustomerAddress.DoesNotExist:
                address = CustomerAddress.objects.create(
                    customer=customer,
                    country=self.request.data['country'],
                    city=self.request.data['city'],
                    post_code=self.request.data['post_code'],
                    address=self.request.data['address']
                )

            order.customer_shipping_address = address
            order.is_ordered = True
            order.time_checkout = datetime.now()
            order.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        except BaseException as error:
            return Response({
                'message': str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
