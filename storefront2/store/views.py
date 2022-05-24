from ast import Add
from select import select
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status

from .permissions import FullDJangoModelPermissions, IsAdminOrReadOnly, ViewCustomerHistoryPermission

from .pagination import DefaultPagination
from .filters import ProductFilter
from .models import Cart, CartItem, Collection, Customer, Order, OrderItem, Product, Review
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, CreateOrderSerializer, CustomerSerializer, OrderSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer

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


# Generic View for Getting all Products / Create a Product
#With this implementation we can delete the 2 methods GET,POST
class ProductList(ListCreateAPIView):
  # We have 2 attributes queryset and serializer_class and we want to simply return an expression or class
  #We added the "select_related" when we wanted to add the title of each Collection
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
# Using ViewSets for combining logic of multiple Generic views for Products
#We end up with single class for implementing Products Endpoint
class ProductViewSet(ModelViewSet):
  # Bringing back the queryset
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] 
  # With the backend above all we have to do is specify the fields use for filtering, removing our filtering logic
  # Now for our custom filtering for multiple values we use "filterset_class" instead of "filterset_fields"
  filterset_class = ProductFilter
  pagination_class = DefaultPagination
  # Applying the custom permission to this view
  permission_classes = [IsAdminOrReadOnly]
  # Setting up the search text based fields the search is case insensitive
  search_fields = ['title', 'description']
  # Specifying the ordering fields
  ordering_fields = ['unit_price', 'last_update']

  def get_serializer_context(self):
      return {'request': self.request}

  # We need to overwrite the destroy() method, using this new class in the ViewSet
  def destroy(self, request, *args, **kwargs):
    # Changing the validation logic to not retrieve get_object twice
    #From the kwargs argument we can read the pk argument
    if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
      return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    return super().destroy(request, *args, **kwargs)

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


# Generic View for Get-Update-Delete a Product
class ProductDetail(RetrieveUpdateDestroyAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  # If we still want to call our parameter ID instead of pk
  #lookup_field = 'id'

  # Overwriting the delete method inherit from the "RetrieveUp..." class to implement our delete logic
  def delete(self, request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.orderitems.count() > 0:
      return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
""" 



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


# Generic View for Getting all Collections / Create a Collection
class CollectionList(ListCreateAPIView):
  queryset = Collection.objects.annotate(products_count=Count('products')).all()
  serializer_class = CollectionSerializer
"""
# Using ViewSets for combining logic of multiple Generic views for Collections
#Using ModelViewSet can perform all kind operations on resources, If we don't want to have WRITE operations we can use "ReadOnlyModelViewSet" class
class CollectionViewSet(ModelViewSet):
  queryset = Collection.objects.annotate(products_count=Count('products')).all()
  serializer_class = CollectionSerializer
  permission_classes = [IsAdminOrReadOnly]

  def destroy(self, request, *args, **kwargs):
    if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
      return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    return super().destroy(request, *args, **kwargs)

"""
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


# Generic View for Get-Update-Delete a Collection
class CollectionDetail(RetrieveUpdateDestroyAPIView):
  queryset = Collection.objects.annotate(products_count=Count('products'))
  serializer_class = CollectionSerializer

  def delete(self, request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if collection.products.count() > 0:
      return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    collection.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
"""



# Creating ViewSet for Reviews
class ReviewViewSet(ModelViewSet):
  # In this field we have access to URL parameters, so we can read the product ID from the URL and using a
  #context object we can pass it to the serializer
  #Remember we use a context object to provide additional data to a serializer
  serializer_class = ReviewSerializer

  # We need to overwrite the queryset method to only the reviews for each product
  def get_queryset(self):
      # Applying a filter to get the reviews in each product 
      return Review.objects.filter(product_id=self.kwargs['product_pk'])

  # Overwriting the serializer context method
  def get_serializer_context(self):
      # The kwargs is a dictionary that contains our url parameters
      return {'product_id': self.kwargs['product_pk']}


# Create a Custom ViewSet for Carts
#We're not going to inherit from ModelViewSet because this class provides all operations, we only need to support
#Create, Get a cart and Delete
class CartsViewSet(CreateModelMixin, 
                   RetrieveModelMixin, 
                   DestroyModelMixin, 
                   GenericViewSet):
  # We need to user eager loading so when retrieving a cart we want to eager load that cart with those items and products
  #In the queryset we call "prefetch_related" bc a cart can have multiple items (for FK where we have single related object we can use select_related)
  #We want to prefetch a cart with "items" and for each item we also wanna preload a product so we add "__product"
  queryset = Cart.objects.prefetch_related('items__product').all()
  serializer_class = CartSerializer


# Creating ViewSet for a CartItem
class CartItemViewSet(ModelViewSet):
  # Preventing PUT requests with the attribute "http_method_names" set it to a list of methods allowed at this endpoint
  http_method_names = ['get', 'post', 'patch', 'delete']

  # Dynamically returning serializer_class depending on the request method
  def get_serializer_class(self):
      if self.request.method == 'POST':
        return AddCartItemSerializer
      if self.request.method == 'PATCH':
        return UpdateCartItemSerializer
      return CartItemSerializer

  # The cart ID it's in the URL in the serializer we don't have access to URL params, so here in the view we get
  #the URL param and using a context object pass it to the serializer
  def get_serializer_context(self):
      # Returning a dictionary with 1 k-v 
      return {'cart_id': self.kwargs['cart_pk']}

  # Overwriting the queryset bc we want to filter by cart ID
  def get_queryset(self):
      # We're gonna extract the cart ID as a URL parameter from "self.kwargs['cart_pk']"
      return CartItem.objects \
        .filter(cart_id=self.kwargs['cart_pk']) \
        .select_related('product')


# ViewSet for the Profile, now we allow all operations but restricted only to admin users but any auth user should be able to access the profile
class CustomerViewSet(ModelViewSet):
  queryset = Customer.objects.all()
  serializer_class = CustomerSerializer
  # We can supply multiple permission classes, if any fails then client will not be able to access this view
  # When we apply this permission the user has to be auth and they should have the relevant model permissions
  #permission_classes = [FullDJangoModelPermissions]
  # We also have [DjangoModelPermissionsOrAnonReadOnly] here anonymous users will have read only access to data
  #All actions in this view set are closed to anonymous users, Only Admin users can manage customers via customers endpoint
  permission_classes = [IsAdminUser]

  # Creating custom action for viewing the history of a particular customer 
  # We use the pk, and detail to True argument because this is for a particular customer
  # Finally we decorate this custom action with our new permission class
  @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
  def history(self, request, pk):
    return Response('ok')


  # Defining a custom action and decorate it with the action decorator in rest framework
  # If we set the detail argument to F, this action is available in the list view: /customers/me, IF detail to T, the action
  #is gonna be available on the detail view: /customers/1/me
  # If we want to we can overwrite the permission in this particular action
  @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
  def me(self, request):
    # Every request has an user attribute, if User not log is then is gonna be set to an instance of the "AnonymousUser" class
    # Retrieving customer with user.id and returning it to the client
    # The "get_or_create" method does not return a customer object it returns a tuple with 2 values: 1) customer object, 2) boolean
    #that tell us if the object was created or not. So we take the tuple and unpacking it immediately to get customer obj
    (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)

    if request.method == 'GET':
      # Serializing customer object
      serializer = CustomerSerializer(customer)
      return Response(serializer.data)
    elif request.method == 'PUT':
      serializer = CustomerSerializer(customer, data=request.data)
      # Validate incoming data
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data)


# View Set for the Orders
class OrderViewSet(ModelViewSet):
  # Applying Permission classes to secure our endpoint
  permission_classes = [IsAuthenticated]

  # Using the Create Order Serializer in this view set overwriting the default serializer
  def get_serializer_class(self):
      if self.request.method == 'POST':
        return CreateOrderSerializer
      return OrderSerializer

  # Overwriting the context to pass the user id
  def get_serializer_context(self):
      return {'user_id': self.request.user.id}

  # If not Admin only seeing it's own orders. So overwriting the queryset
  def get_queryset(self):
      user = self.request.user

      if user.is_staff:
        return Order.objects.all()

      # From the user_id we need to calculate the customer_id, we add the only() method to pick only the id field we need from the object
      # If the current user doesn't have a customer record or a profile, the get() method throw an exception bc expects 1 
      #record in the DB if we have 0 or more than 1 record matching the criteria we get an exception. So we use get_or_create() 
      #which returns a tuple with 2 values: 1) object we're reading 2) boolean indicates if the record was created or not
      (customer_id, created) = Customer.objects.only('id').get_or_create(user_id=user.id)
      # Otherwise we want to apply a filter and retrieve orders for a specific customer
      return Order.objects.filter(customer_id=customer_id)