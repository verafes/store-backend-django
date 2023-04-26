from django.core.management.base import BaseCommand
from products.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("my first command")
        new_brand = Brand.objects.create(title='super brand')
        Product.objects.create(
            title=f'Good product',
            price=100,
            old_price=110,
            quantity=5,
            brand=new_brand,
            description='super description',
            )
        Product.objects.create(
            title=f'new product',
            price=50,
            old_price=60,
            quantity=3,
            brand=new_brand,
            description='just description',
        )