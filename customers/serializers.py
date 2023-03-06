from rest_framework import serializers

from .models import Customer, CustomerAddress
from orders.models import Order, OrderProduct
from django.contrib.auth import get_user_model


User = get_user_model()


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validate_data):
        try:
            user = User.objects.create(
                username=validate_data['username'],
                email=validate_data['email'],
                first_name=validate_data['first_name'],
                last_name=validate_data['last_name']
            )
            try:
                customer = Customer.objects.get(token=self.context['request'].data['token'])
                customer.user = user
                if len(customer.first_name) == 0:
                    customer.first_name = validate_data['first_name']
                if len(customer.last_name) == 0:
                    customer.last_name = validate_data['last_name']
                if len(customer.email) == 0:
                    customer.email = validate_data['email']
                customer.save()
            except BaseException as error:
                print("Error:", str(error))
            user.set_password(validate_data['password'])
            user.save()
            return user

        except BaseException as error:
            print("Error:", str(error))
            return False


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

