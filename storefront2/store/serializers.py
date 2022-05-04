# A Serializer convers a model instance to a dictionary

from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
  # Deciding what fields of the Product class we wanna serialize
  #Defining the fields as we would define them in the model
  id = serializers.IntegerField()
  #Later we use this serializer when receiving data
  title = serializers.CharField(max_length=255)
  #We can name them whatever, it's completely separate object from the Product object
  unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
