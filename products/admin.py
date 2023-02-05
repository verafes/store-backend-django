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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_active']
    search_fields = ['category',]


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'category']
    search_fields = ['product', 'category']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'review', 'fullname', 'product_id']

