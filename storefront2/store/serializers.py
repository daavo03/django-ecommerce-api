# A Serializer convers a model instance to a dictionary

from decimal import Decimal
from rest_framework import serializers
from store.models import CartItem, Customer, Order, OrderItem, Product, Collection, Review, Cart


# Including a Nested Object. First we need to create a class
class CollectionSerializer(serializers.ModelSerializer):
  #Applying the same changes with the ModelSerializer
  class Meta:
    model = Collection
    # Adding new "products_count" field
    fields = ['id', 'title', 'products_count']

  # Because Collection class doesn't have this field we have to define it
  # Because we're using Generic views when creating a Collection this field it's required
  #so we want to mark this field as readonly
  products_count = serializers.IntegerField(read_only=True)

# Using ModelSerializer to quickly create a serializer. To a related field by default it use PK related field 
class ProductSerializer(serializers.ModelSerializer):
  # Creating a meta class
  class Meta:
    model = Product
    # An array or tuple of the fields to include
    #Including a field does not exist, we add it and define it below
    fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']

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

  #The save() method will call one of these methods depending on the state of the serializer
  #Overwriting how a product is created
  # def create(self, validated_data):
  #     # Create a "product" object and unpacking the dictionary
  #     product = Product(**validated_data)
  #     product.other = 1
  #     product.save()
  #     return product

  # #Overwriting how a product is updated
  # def update(self, instance, validated_data):
  #     instance.unit_price = validated_data.get('unit_price')
  #     instance.save()
  #     return instance

# Serializer for the Reviews
class ReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Review
    # We remove the product field because we want it to be autoimported
    fields = ['id', 'date', 'name', 'description']

  # Now we want to overwrite the create method for creating a review
  def create(self, validated_data):
      # Instead of relying in default implementation getting the values from fields we want to provide our own implementation
      #First we're gonna read product_id
      product_id = self.context['product_id']
      #Then we can pass multiple k-v pairs, so we set the "product_id" to the value above, and then unpack the validated_data
      #dictionary that we receive
      return Review.objects.create(product_id=product_id, **validated_data)


# Defining new Serializer for serializing a Product in a Shopping CartItem  
class SimpleProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    # only see the fields we want when returning a cart
    fields = ['id', 'title', 'unit_price']


# New Serializer for the CartItems we put it above the cart serializer bc we need to use it in it
class CartItemSerializer(serializers.ModelSerializer):
  # Redefining product field to see the product object
  product = SimpleProductSerializer()
  # Adding the total price for each item, which is going to be a calculated field
  total_price = serializers.SerializerMethodField()

  # With the fields like "total_price" above we can follow a particular convention for defining the method that returns
  #the value for this field "get_nameOfTheField"
  def get_total_price(self, cart_item:CartItem):
    return cart_item.quantity * cart_item.product.unit_price

  class Meta:
    model = CartItem
    fields = ['id', 'product', 'quantity', 'total_price']



# New Serializer for the cart
class CartSerializer(serializers.ModelSerializer):
  # Declaring this field as read only, so that we don't have to send it to the server we're only going to read it from the server 
  id = serializers.UUIDField(read_only=True)
  # Defining explicitly the items field with many=True to see actual cart items, also marking it as read_only
  items = CartItemSerializer(many=True, read_only=True) 
  # Total price for our cart
  total_price = serializers.SerializerMethodField()

  def get_total_price(self, cart):
    # Here we add a list comprehension, the collection here is "cart.items.all()" bc cart.items returns a manager object, so
    #using all we get the queryset which returns all the items
    # Then for each item instead of returning the item we want to return the quantity times unit_price
    # With the final expression we get a list of totals, so we need to sum all of them
    return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
  class Meta:
    model = Cart
    # Returning to the client only the id, Adding 'items' field to returning the cart items
    fields = ['id', 'items', 'total_price']


# Serializer for adding items to cart
class AddCartItemSerializer(serializers.ModelSerializer):
  # Explicitly defining product_id field
  product_id = serializers.IntegerField()

  # Validate invalid fields with "validate_fieldName(self, valueValidating(in this case product_id))"
  def validate_product_id(self, value):
    if not Product.objects.filter(pk=value).exists():
      raise serializers.ValidationError('No product with the given id was found')
    return value

  # Overwriting the save method to nor create multiple cart item records, we want to update quantity of existing item
  def save(self, **kwargs):
      # Reading the Cart ID
      cart_id = self.context['cart_id']

      # Here we need to get the product_id and quantity
      #Behind the scenes there's a call to serializer.is_valid(), when data gets validated then we can get it from an 
      #attribute "validated_data". BC currently we're inside our serializer class so we say "self.validated_data" which
      #is a dictionary and from there we can read the "product_id" received from the client
      product_id = self.validated_data['product_id']
      quantity = self.validated_data['quantity']

      # Saving logic
      #If there's no such cart item it wil throw exception so wrap all this inside a try/except block
      try:
        cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
        # Update an existing item
        cart_item.quantity += quantity
        cart_item.save()
        self.instance = cart_item
      except CartItem.DoesNotExist:
        # Create a new item
        self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

      return self.instance
  class Meta:
    model = CartItem
    fields = ['id', 'product_id', 'quantity']

# Custom Serializer for Updating Cart Item
class UpdateCartItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = CartItem
    fields = ['quantity']


# Serializer for the Profile 
class CustomerSerializer(serializers.ModelSerializer):
  # Explicitly defining the "user_id" field even though we have the attribute in the Customer Model bc is created dynamically at runtime
  # Also marking it as "read_only" bc we don't want to associate this profile with someone's else account
  user_id = serializers.IntegerField(read_only=True)

  class Meta:
    model = Customer
    fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']

# Serializer for the OrderItem
class OrderItemSerializer(serializers.ModelSerializer):
  # Changing the product to a nested object to return all critic info about each product so client doesn't have to send
  #additional requests to each product in the Order
  product = SimpleProductSerializer()


  class Meta:
    model = OrderItem
    # We're not including order here bc we're gonna use this serializer inside our Order Serializer
    fields = ['id', 'product', 'unit_price', 'quantity']


# Serializer for the Orders
class OrderSerializer(serializers.ModelSerializer):
  items = OrderItemSerializer(many=True)
  class Meta:
    model = Order
    fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']