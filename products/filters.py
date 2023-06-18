import django_filters
from .models import Product


class ProductFilter(django_filters.rest_framework.FilterSet):
    """
    A filter class for filtering instances of the Product model based on various criteria.
    Supports filtering by minimum price, maximum price, brand, title, and brand ID.
    """
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    brand = django_filters.CharFilter(field_name='brand__title', lookup_expr='contains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='contains')
    brand_id = django_filters.NumberFilter(field_name='brand_id', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ('min_price', 'max_price', 'brand', 'title', 'brand_id')
