from django.contrib import admin
from . import models

# Using the register decorator on this class
#With this we're saying that this class above is the Admin Model for the Product class, now we don't need the last
#line anymore
@admin.register(models.Product)
# How we wanna view or edit our model(in this case Products)
class ProductAdmin(admin.ModelAdmin):
  # Set a bunch of attributes to customize the list page
  #We got a new column where we can see the price of each Product
  list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
  # Fields that can be edited on the list page
  list_editable = ['unit_price']
  # Get 10 Products per page
  list_per_page = 10

  # To implement sorting we apply the admin display decorator to the method
  @admin.display(ordering='inventory')
  def inventory_status(self, product):
    if product.inventory < 10:
      return 'Low'
    return 'Ok'
  
  # We set this to the list of fields we want to eagerload
  list_select_related = ['collection']

  # Displaying a specific field
  def collection_title(self, product):
    return product.collection.title


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
  list_display = ['first_name', 'last_name', 'membership']
  list_editable = ['membership']
  ordering = ['first_name', 'last_name']
  list_per_page = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ['id', 'placed_at', 'customer']

# Registering the models for the admin site
admin.site.register(models.Collection)