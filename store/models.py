from django.db import models

# We don't have an ID field in any class, because django creates it for us automatically
# Define a new class and having inherit the Model class in django
class Product(models.Model):
  # Define the fields of this class
  title = models.CharField(max_length = 255)
  description = models.TextField()
  price = models.DecimalField(max_digits = 6, decimal_places = 2) #Always use DecimalField() for monetary values
  inventory = models.IntegerField()
  last_update = models.DateTimeField(auto_now = True) #auto_now=True every time we update a product object django auto stores current datetime

class Customer(models.Model):
  first_name = models.CharField(max_length = 255)
  last_name = models.CharField(max_length = 255)
  email = models.EmailField(unique = True)
  phone = models.CharField(max_length = 255)
  birth_date = models.DateField(null = True) #We don't care about the time they born that's why we use DateField()
