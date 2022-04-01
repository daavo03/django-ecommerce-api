from django.db import models

# We don't have an ID field in any class, because django creates it for us automatically

# Define a new class and having inherit the Model class in django
class Product(models.Model):
  # Define the fields of this class
  title = models.CharField(max_length=255)
  description = models.TextField()
  price = models.DecimalField(max_digits=6, decimal_places=2) #Always use DecimalField() for monetary values
  inventory = models.IntegerField()
  last_update = models.DateTimeField(auto_now=True) #auto_now=True every time we update a product object django auto stores current datetime

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