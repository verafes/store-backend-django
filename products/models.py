from django.db import models


""" Table of Products """
class Product(models.Model):
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


""" Table of Brands """
class Brand(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Title")

    class Meta:
        db_table = 'brands'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.title


""" Table Category """
class Category(models.Model):
    title = models.CharField(verbose_name='Category', max_length=200, blank=False, null=False)
    is_active = models.BooleanField(verbose_name='Is Active', default=False, blank=False, null=False)

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


""" Table of relationship between Products-Category """
class ProductCategory(models.Model):
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


""" Table of Reviews of Products """
class ProductReview(models.Model):
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
        # return str(self.product) + " - " + self.review[0.5] + ".."
