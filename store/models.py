from tkinter import CASCADE
from django.db import models

# We don't have an ID field in any class, because django creates it for us automatically

# New class "Promotion" and define m-m RS to Product. So a product can have different promotions, and a Promotion can apply to different Products
#We can define the RS in either class
class Promotion(models.Model):
  description = models.CharField(max_length=255)
  discount = models.FloatField()


# To implement the other R.S
class Collection(models.Model):
  title = models.CharField(max_length=255)
  featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+') #If we delete a product and that product happens to be the featured product for Collection we want to set it to null
  #if we don't care about the reverse relationship we can simply type a plus sign. This tells django not to create that reverse RS

# Define a new class and having inherit the Model class in django
class Product(models.Model):
  # Define the fields of this class
  title = models.CharField(max_length=255)
  slug = models.SlugField() #default option "default='-'"
  description = models.TextField()
  # We change the name from "price" to "unit_price" and run the `python manage.py makemigrations`
  unit_price = models.DecimalField(max_digits=6, decimal_places=2) #Always use DecimalField() for monetary values
  inventory = models.IntegerField()
  last_update = models.DateTimeField(auto_now=True) #auto_now=True every time we update a product object django auto stores current datetime
  # Here we have a dependency from the Product class towards the Collection class
  collection = models.ForeignKey(Collection, on_delete=models.PROTECT) #If we delete a collection we don't end up deleting all the products in that collection
  promotions = models.ManyToManyField(Promotion) #If we wanna change the name of the FK in the Promotion class we can use "related_name='products'"

class Customer(models.Model):
  #We define the values of the choices separately.
  #Here we store the actual value
  MEMBERSHIP_BRONZE = 'B'
  MEMBERSHIP_SILVER = 'S'
  MEMBERSHIP_GOLD = 'G'

  #Defining a new attribute, we use uppercase to indicate this is a fix list of values
  #We can reference in multiple places like here
  MEMBERSHIP_CHOICES = [
    (MEMBERSHIP_BRONZE, 'Bronze'),
    (MEMBERSHIP_SILVER, 'Silver'),
    (MEMBERSHIP_GOLD, 'Gold'),
  ]
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.EmailField(unique=True)
  phone = models.CharField(max_length=255)
  birth_date = models.DateField(null=True) #We don't care about the time they born that's why we use DateField()
  membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE) #Once we have the array we can add the choices option

  # Defining metadata about this model, adding an inner class
  class Meta:
    db_table = 'store_customers'
    # We use them to speed up our querys
    indexes = [
      models.Index(fields=['last_name', 'first_name'])
    ]

class Order(models.Model):
  #Our constants
  PAYMENT_STATUS_PENDING = 'P'
  PAYMENT_STATUS_COMPLETE = 'C'
  PAYMENT_STATUS_FAILED = 'F'
  PAYMENT_STATUS_CHOICES = [
    (PAYMENT_STATUS_PENDING, 'Pending'),
    (PAYMENT_STATUS_COMPLETE, 'Complete'),
    (PAYMENT_STATUS_FAILED, 'Failed'),
  ]

  #Our fields
  placed_at = models.DateTimeField(auto_now_add=True)
  payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
  customer = models.ForeignKey(Customer, on_delete=models.PROTECT) #If we delete a customer we don't end up deleting orders

class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.PROTECT)
  product = models.ForeignKey(Product, on_delete=models.PROTECT)
  quantity = models.PositiveSmallIntegerField() #With this field we can prevent negative values from been stored in this field
  unit_price = models.DecimalField(max_digits=6, decimal_places=2)



# Implementing 1-1 RS within 2 models
class Address(models.Model):
  #Assume that every customer should have 1 address, each address should belong to 1 customer
  street = models.CharField(max_length=255)
  city = models.CharField(max_length=255)
  zip = models.PositiveIntegerField(null=True)
  #Specifying the parent in the child class
  # Let's assume a customer can have multiple addresses so we change the type of the field to "ForeignKey"
  #so we're telling django that "customer" it's a Foreign Key in this table,
  #also we remote the "primary_key" because we wanna have multiple addresses for the same customer, so we wanna allow multiple values for this column
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE) #When we delete a customer if on_delete on CASCADE the address also deleted, 
  #if the field accept null values we can use SET_NULL, so when we delete a customer(parent record) the child record it's not going to get delted and
  #the customer column it's gonna set to null, PROTECT we can prevent the deletion is there's a child associate wit this parent we cannot delete that parent
  #first we have to delete the child
  #If we don't set the "primary_key" to True django will create another field ID so every address is gonna have an ID and that means we'll end up
  #with 1-many RS between customers and addresses, because we can have many addresses with the same customer
  # We don't have to go to Customers to set the reverse RS, No, django auto creates this for us

class Cart(models.Model):
  created_at = models.DateTimeField(auto_now_add=True) #This field gets autopopulated when we create a new cart

class CartItem(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE) #Here we use CASCADE so if we delete a cart we don't need it anymore we should delete all items auto
  product = models.ForeignKey(Product, on_delete=models.CASCADE) #If we can delete a product, if that product has never been order before then that product should be remove from all the existing shopping carts
  quantity = models.PositiveSmallIntegerField()