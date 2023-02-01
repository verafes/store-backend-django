from django.contrib import admin

from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'old_price', 'description', 'quantity', 'brand_id']
    search_fields = ['title',]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title',]

""" 
admin.site.register(Product, ProductAdmin)
"""
