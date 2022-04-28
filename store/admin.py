from django.contrib import admin
from . import models

# Registering the models for the admin site
admin.site.register(models.Collection)
admin.site.register(models.Product)