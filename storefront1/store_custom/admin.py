from store.models import Product
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from tags.models import TaggedItem

# Here we're going to combine features from the 2 plugable apps

# Moving this class to our new app (here) because this is where we're referencing the TaggedItem class
# Managing the Tags on our Product form
#Creating inline class for managing a tag
class TagInline(GenericTabularInline):
  # Changing the tags in the form to autocomplete
  autocomplete_fields = ['tag']
  model = TaggedItem


# Creating new ProductAdmin which extends the generic ProductAdmin that comes with our reusable app
#In this new implementation we're going to reference the TagInline class
class CustomProductAdmin(ProductAdmin):
  inlines = [TagInline]

# With the new ProductAdmin we need to unregister the old one and register the new one
admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)