from django.db import models


class Product(models.Model):
    """ Table of Products """
    title = models.CharField(verbose_name='Title', max_length=200, null=False, blank=False)
    price = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=False, blank=False)
    old_price = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=False, blank=False)
    brand = models.ForeignKey('products.Brand', null=True, blank=False, on_delete=models.SET_NULL)
    photo = models.FileField(verbose_name='Photo', null=True, blank=True)
    quantity = models.IntegerField(default=1, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['id',]

    def __str__(self):
        return self.title


class Brand(models.Model):
    """ Table of Brands """
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Title")

    class Meta:
        db_table = 'brands'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.title


class Category(models.Model):
    """ Table Category """
    title = models.CharField(verbose_name='Category', max_length=200, blank=False, null=False)
    is_active = models.BooleanField(verbose_name='Is Active', default=False, blank=False, null=False)

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    """ Table of relationship between Products-Category """
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE, blank=False, null=False)
    category = models.ForeignKey(Category, related_name='category_products', verbose_name='Category',
                                 on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        db_table = 'product_category'
        verbose_name = 'Product Category'
        verbose_name_plural = 'Products Categories'

    def __str__(self):
        return self.product.title
               # + " - " + str(self.category.title)[0:5]


class ProductReview(models.Model):
    """ Table of Reviews of Products """
    review = models.CharField(verbose_name='Review', max_length=200000, blank=False, null=False)
    fullname = models.CharField(verbose_name='Full name', max_length=200, blank=False, null=False)
    product = models.ForeignKey(Product, related_name='reviews', verbose_name='Product',
                                on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        db_table = 'product_review'
        verbose_name = 'Product review'
        verbose_name_plural = 'Products reviews'

    def __str__(self):
        # return self.fullname
        return self.product.title
