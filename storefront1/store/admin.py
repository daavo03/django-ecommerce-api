from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models


# Creating our own custom filters
class InventoryFilter(admin.SimpleListFilter):
  # Setting attributes
  title = 'inventory'
  parameter_name = 'inventory'

  # 2 methods to implement here
  #lookups we can specify what items should appear in the list
  def lookups(self, request, model_admin):
      return [
        # Each tuple represents 1 of the filters in the list
        #In each should have 2 values: actual value for filter, human readable descrip
        ('<10', 'Low')
      ]

  #queryset implementing filtering logic
  def queryset(self, request, queryset):
      # This returns the selected filter
      if self.value() == '<10':
        return queryset.filter(inventory__lt=10)


# Using the register decorator on this class
#With this we're saying that this class above is the Admin Model for the Product class, now we don't need the last
#line anymore
@admin.register(models.Product)
# How we wanna view or edit our model(in this case Products)
class ProductAdmin(admin.ModelAdmin):
  # Customizing the forms
  #Selecting the fields to show in the form
  #fields = ['title', 'slug']
  #Excluding certain fields
  #exclude = ['promotions']
  #We also have readonly fields
  #readonly_fields = ['title']
  #Autocompleting fields
  autocomplete_fields = ['collection']
  #Specifying how each field in the form can get prepopulated
  prepopulated_fields = {
    'slug': ['title']
  }
  # To show the list of actions to the user
  actions = ['clear_inventory']
  # Set a bunch of attributes to customize the list page
  #We got a new column where we can see the price of each Product
  list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
  # Fields that can be edited on the list page
  list_editable = ['unit_price']
  # Filtering the products
  #To use our custom filter we type the name of the class in this list
  list_filter = ['collection', 'last_update', InventoryFilter]
  # Get 10 Products per page
  list_per_page = 10
  search_fields = ['title']

  # To implement sorting we apply the admin display decorator to the method
  @admin.display(ordering='inventory')
  def inventory_status(self, product):
    if product.inventory < 10:
      return 'Low'
    return 'Ok'

  # Creating a custom action
  #The description is the text to appear in the dropdown list
  @admin.action(description='Clear inventory')
  def clear_inventory(self, request, queryset):
    # This will update DB and return the number of updated records
    updated_count = queryset.update(inventory=0)
    # Show a msg to the user
    self.message_user(
      # First argument request object
      request,
      # Message show to the user
      f'{updated_count} products were successfully updated.',
      # To select the type of message
      #messages.ERROR
    )
  
  # We set this to the list of fields we want to eagerload
  list_select_related = ['collection']

  # Displaying a specific field
  def collection_title(self, product):
    return product.collection.title


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
  list_display = ['first_name', 'last_name', 'membership', 'orders']
  list_editable = ['membership']
  list_per_page = 10
  ordering = ['first_name', 'last_name']
  search_fields = ['first_name__istartswith', 'last_name__istartswith']

  @admin.display(ordering='orders_count')
  def orders(self, customer):
    url = (
      reverse('admin:store_order_changelist')
      + '?'
      + urlencode({
        'customer_id': str(customer.id)
      })
    )
    return format_html('<a href="{}">{}</a>', url, customer.orders_count)
  
  def get_queryset(self, request):
      return super().get_queryset(request).annotate(
        orders_count=Count('order')
      )


# We also can use StackedInLine in which each item will be represented as a separated form
class OrderItemInLine(admin.TabularInline):
  autocomplete_fields = ['product']
  model = models.OrderItem
  # Don't see the placeholders
  extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
  autocomplete_fields = ['customer']
  # Setting min and max number of items for order
  min_num = 1
  max_num = 10
  # Adding the OrderItemInLine class as an inline
  inlines = [OrderItemInLine]
  list_display = ['id', 'placed_at', 'customer']

# Registering the models for the admin site
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
  list_display = ['title', 'products_count']
  # Adding the attribute for searching collections in the Products
  search_fields = ['title']

  # Defining a method to treat the computed field
  @admin.display(ordering='products_count')
  def products_count(self, collection):
    # Sending our users to the products page
    # Applying a filter
    url = (
      #app_model_page 
      reverse('admin:store_product_changelist')
      + '?'
      # Here we need to generate the querystring parameters
      #We give it a dictionary because a querystring can contain
      #multiple k-v pairs
      + urlencode({
        'collection__id': str(collection.id)
      }))  
    # Generate a HTML link
    return format_html('<a href="{}">{}</a>', url, collection.products_count)     

  # So we need to overwrite the queryset on this page
  #Every ModelAdmin has a method called "get_queryset"
  def get_queryset(self, request):
      return super().get_queryset(request).annotate(
        products_count=Count('product')
      )

