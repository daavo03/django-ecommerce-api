# A Serializer convers a model instance to a dictionary

from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection


# Including a Nested Object. First we need to create a class
class CollectionSerializer(serializers.ModelSerializer):
  #Applying the same changes with the ModelSerializer
  class Meta:
    model = Collection
    fields = ['id', 'title']

# Using ModelSerializer to quickly create a serializer. To a related field by default it use PK related field 
class ProductSerializer(serializers.ModelSerializer):
  # Creating a meta class
  class Meta:
    model = Product
    # An array or tuple of the fields to include
    #Including a field does not exist, we add it and define it below
    fields = ['id', 'title', 'unit_price', 'price_with_tax', 'collection']

  price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

  # # Deciding what fields of the Product class we wanna serialize
  # #Defining the fields as we would define them in the model
  # id = serializers.IntegerField()
  # #Later we use this serializer when receiving data
  # title = serializers.CharField(max_length=255)
  # #We can name them whatever, it's completely separate object from the Product object with argument "source"
  # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
  # # New field defining a new method which will return a value for this field
  # # Including relating objects like "collection" with this we can include the PK or the ID of each collection in
  # #a product object
  # #collection = serializers.PrimaryKeyRelatedField(
  #   # Setting the argument for looking collections
  #   #queryset = Collection.objects.all()
  # #)
  # #Another way is to return a collection as a string, returning the name of each collection
  # #collection = serializers.StringRelatedField()
  # # Including a nested object
  # #collection = CollectionSerializer()
  # # Including a link to an endpoint for viewing that Collection
  # collection = serializers.HyperlinkedRelatedField(
  #   queryset = Collection.objects.all(),
  #   # This argument is used for generating hyperlink
  #   view_name='collection-detail'
  # )


  #Defining the method
  def calculate_tax(self, product: Product):
    return product.unit_price * Decimal(1.1)
