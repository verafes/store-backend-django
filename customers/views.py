from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
import uuid
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from .models import Customer, CustomerAddress
from .serializers import CustomerSerializer, MyOrderSerializer, CustomerAddressSerializer
from orders.models import Order


'''Create customer > api/customer/create'''
class CustomerCreate(APIView):
    HTTP_method_names = ['post']

    def post(self, *args, **qargs):
        client_ip = self.request.META.get('REMOTE_ADDR')
        client_agent = self.request.META.get('HTTP_USER_AGENT')
        print('IP:', client_ip)
        print('client agent:', client_agent)

        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)
        response = {
            'status': True,
            'customer_token': customer_token,
        }
        return Response(status=HTTP_201_CREATED, data=response)


class GetAuthCustomer(generics.RetrieveAPIView):
    serializer_class = CustomerSerializer


'''List of orders - api/customer/myorders/'''
class MyOrders(generics.ListAPIView):
    serializer_class = MyOrderSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(customer__user=self.request.user)


'''List of Customers - api/customer/list'''
class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


'''List of Customer's Addresses - api/customer/address/list'''
class CustomerAddressList(generics.ListAPIView):
    queryset = CustomerAddress.objects.all()
    serializer_class = CustomerAddressSerializer
