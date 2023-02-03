from django.contrib import admin
from .models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'time_created', 'time_checkout', 'time_delivery',
                    'is_ordered', 'customer_id', 'customer_shipping_address_id']
    search_fields = ['time_checkout', 'time_delivery', 'customer_id']


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'product_id', 'price', 'quantity']
    search_fields = ['order_id', 'product_id']
