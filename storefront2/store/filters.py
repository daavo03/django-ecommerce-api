from django_filters.rest_framework import FilterSet

from .models import Product

class ProductFilter(FilterSet):
  class Meta:
    model = Product
    fields = {
      # We use dictionary bc for each field we can specify how the filtering should be done
      'collection_id': ['exact'],
      'unit_price': ['gt', 'lt']
    }