from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

# Passing an array of strings that specify the HTTP methods we support at this method
@api_view(['GET', 'POST'])
# Here we should create a view function (take a request returns a response)
def product_list(request):
  if request.method == 'GET':
    # Getting all Products
    # Loading Products and their Collections together using "select_related()"
    queryset = Product.objects.select_related('collection').all()
    # Giving the serializer a queryset, the "many=True" to knows it should iterate over this queryset and convert each
    #product object to a dictionary
    # We need to pass our request object to our serializer
    serializer = ProductSerializer(queryset, many=True, context={'request': request})
    # Here we return a response object
    return Response(serializer.data)
  elif request.method == 'POST':
    # Here the deserialization happens
    #To deserialize data we have to set the "data=" to request.data
    serializer = ProductSerializer(data=request.data)
    # If there's invalid data django restframework is automatic return response with 400 status including validation errors
    serializer.is_valid(raise_exception=True)
    # The save() method has some logic for extracting data from the dictionary to create/update a product
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

"""  
# Create another view function for seeing details of a product
@api_view()
#Giving the id parameter
def product_detail(request, id):
  # Wrapping the code in try-catch block
  try:
    # Modifying the view function, getting the product with the ID
    product = Product.objects.get(pk=id)
    # Creating a Serializer and give it this "product" object
    serializer = ProductSerializer(product)
    # Getting the dictionary
    #serializer.data
    # Returning the id in the response verify all works
    # Instead of including the ID in the res, we'll include "serializer.data"
    return Response(serializer.data)
  # Catching an exception of type "DoesNotExist"
  except Product.DoesNotExist:
    # We just need to set the status to 404
    return Response(status=status.HTTP_404_NOT_FOUND)
"""

# Updating a product
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
  # Using our shortcut function
  product = get_object_or_404(Product, pk=id)
  # Checking the request method
  if request.method == 'GET':
    # We give this Serializer a product object
    serializer = ProductSerializer(product)
    return Response(serializer.data)
  elif request.method == 'PUT':
    # Deserializing and also passing a product instance
    serializer = ProductSerializer(product, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
  elif request.method == 'DELETE':
    # Before we delete a product we should check to see if there any orderitems associated with this product
    if product.orderitems.count() > 0:
      return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



# Creating the view for collection_detail
@api_view()
#Changing the id for pk as well 
def collection_detail(request, pk):
  return Response('ok')