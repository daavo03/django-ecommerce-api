from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer

""" 
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

"""
# Converting function view to class view
#Defining the class
class ProductList(APIView):
  #Method for handling GET request
  def get(self, request):
    queryset = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

  #Method for handling POST request
  def post(self, request):
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
"""

# Generic View for Getting all Products / Create a Product
#With this implementation we can delete the 2 methods GET,POST
class ProductList(ListCreateAPIView):
  # We have 2 attributes queryset and serializer_class and we want to simply return an expression or class
  queryset = Product.objects.select_related('collection').all()
  serializer_class = ProductSerializer

  # This methods are useful if we want to have some logic,condition for creating a queryset
  # Maybe checking current user and depending on current user and their permissions provide diff querysets
  #Overwriting queryset
  #def get_queryset(self):
      #return Product.objects.select_related('collection').all()

  # Maybe diff users and diff roles can have diff serializer classes
  #Overwriting serializer
  #def get_serializer_class(self):
      #return ProductSerializer()

  # While creating this "ProductSerializer" we need to pass a context object. So we can overwrite
  #the "get_serializer_context" and return our context object (dictionary that contains the request object)
  def get_serializer_context(self):
      return {'request': self.request}



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
"""

# Get-Update-Delete a Product
class ProductDetail(APIView):
  def get(self, request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

  def put(self, request, id):
    product = get_object_or_404(Product, pk=id)

    serializer = ProductSerializer(product, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

  def delete(self, request, id):
    product = get_object_or_404(Product, pk=id)

    if product.orderitems.count() > 0:
      return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  


""" 
# Getting all Collections / Create a Collection
@api_view(['GET', 'POST'])
def collection_list(request):
  if request.method == 'GET':
    # We're gonna get all our collections and annotate them with the number of products in each Collection
    # Also note the "products" attribute we overwrote Django convention for naming related fields
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer = CollectionSerializer(queryset, many=True)
    return Response(serializer.data)
  elif request.method == 'POST':
    serializer = CollectionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
"""

# Generic View for Getting all Collections / Create a Collection
class CollectionList(ListCreateAPIView):
  queryset = Collection.objects.annotate(products_count=Count('products')).all()
  serializer_class = CollectionSerializer



# Get-Update-Delete a Collection
# Creating the view for collection_detail
@api_view(['GET', 'PUT', 'DELETE'])
#Changing the id for pk as well 
def collection_detail(request, pk):
  # As 1st argument we're passing the same queryset we use earlier
  collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
  if request.method == 'GET':
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = CollectionSerializer(collection, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
  elif request.method == 'DELETE':
    # Before deleting we're checking the collection has any products
    if collection.products.count() > 0:
      return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    collection.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



