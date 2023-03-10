from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Customer(models.Model):
    first_name = models.CharField(verbose_name='First Name', max_length=200, default='', blank=True, null=True)
    last_name = models.CharField(verbose_name='Last Name', max_length=200, default='', blank=True, null=True)
    phone = models.BigIntegerField(verbose_name='Phone number', null=True, blank=True)
    email = models.CharField(verbose_name='Email', max_length=200, default='', blank=True, null=True)
    time_created = models.DateTimeField(verbose_name='Date', auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE, null=True, blank=True)
    token = models.CharField(max_length=200, null=False, blank=False, verbose_name='Token', default='')

    class Meta:
        db_table = 'customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.last_name


class CustomerAddress(models.Model):
    country = models.CharField(verbose_name='Country', max_length=60, blank=False, null=False)
    city = models.CharField(verbose_name='City', max_length=30, blank=False, null=False)
    address = models.CharField(verbose_name='Street Address', max_length=200, blank=False, null=False)
    post_code = models.CharField(verbose_name='Post code', max_length=10, blank=False, null=False)
    customer = models.ForeignKey(Customer, verbose_name='Customer', on_delete=models.CASCADE,
                                 blank=False, null=False)

    class Meta:
        db_table = 'customer_address'
        verbose_name = 'Customer Address'
        verbose_name_plural = 'Customers Addresses'

        def __str__(self):
            return str(self.address)