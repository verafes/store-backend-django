from django.contrib import admin
from .models import *


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['token', 'id', 'first_name', 'last_name', 'phone', 'email', 'time_created', 'user_id']
    search_fields = ['first_name', 'last_name', 'phone', 'email', 'title']


@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'country', 'city', 'address', 'post_code', 'customer']
    search_fields = ['country', 'city', 'address', 'post_code']

