from django.contrib import admin
from .models import Tag

# Register our Tag model so we can manage our tags in the admin interface
@admin.register(Tag)
# Creating an admin class for our Tag model
class TagAdmin(admin.ModelAdmin):
  search_fields = ['label']