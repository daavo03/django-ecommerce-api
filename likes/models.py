from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class LikedItem(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  # content_type for identifying the type of an object that the user likes
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  # object_id for referencing that particular object
  object_id = models.PositiveIntegerField()
  # content_object for reading that actual object
  content_object = GenericForeignKey() 
