from django.db import models

from products.models import Product
from customers.models import Customer, CustomerAddress


class Order(models.Model):
    customer = models.ForeignKey(Customer, verbose_name="Customer", on_delete=models.CASCADE, blank=False, null=False)
    customer_shipping_address = models.ForeignKey(CustomerAddress, verbose_name="Customer shipping address",
                                                  on_delete=models.SET_NULL, blank=True, null=True)
    time_created = models.DateTimeField(verbose_name='Created Date', auto_now_add=True, blank=True, null=True)
    time_checkout = models.DateTimeField(verbose_name='Checkout Date', auto_now_add=True, blank=True, null=True)
    time_delivery = models.DateTimeField(verbose_name='Delivery Date', auto_now_add=True, blank=True, null=True)
    is_ordered = models.BooleanField(verbose_name='Is Ordered', default=False)

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'orders'

        def __str__(self):
            return str(self.customer)


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE, blank=False, null=False)
    order = models.ForeignKey(Order, verbose_name='Order', on_delete=models.CASCADE, blank=False, null=False)
    price = models.DecimalField(verbose_name='Price', default=0, decimal_places=2, max_digits=10)
    quantity = models.IntegerField(verbose_name='Quantity', default=0, blank=False, null=False)

    class Meta:
        db_table = 'order_product'
        verbose_name = 'Order Product'
        verbose_name_plural = 'orders Products'
