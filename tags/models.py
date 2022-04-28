from django.db import models
# Importing ContentType
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Creating a Custom Manager
class TaggedItemManager(models.Manager):
  def get_tags_for(self, obj_type, obj_id):
    content_type = ContentType.objects.get_for_model(obj_type)

    return TaggedItem.objects \
      .select_related('tag') \
      .filter(
        content_type=content_type,
        obj_id=obj_id
      )

class Tag(models.Model):
  label = models.CharField(max_length=255)

class TaggedItem(models.Model):
  # Using the Manager in the TaggedItem model
  objects = TaggedItemManager()
  # Using this class we can find out what tag is applied to what object
  tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
  # Identifying the object that this tag is applied to
  #we need a generic way of identifying an object
  #1st thing we need the Type of an object which can be (product, video, article, photo)
  #2nd thing we need the ID of an object 
  #Using these 2 we can identify any objects in our app, we can identify any record in any tables 
  #(Using Type we can find the table, and using the ID we can find the record)
  # So instead of using a concrete model like "Product" we should an abstract model called "ContentType" which comes with django
  #Earlier we talk about the installed apps in the "settings" module, here we have an app called "django.contrib.contentypes"
  #using it we can create generic RS in our models
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  # So "ContentType" is a model that represents the type of an object in our app
  # 2ND attribute we need here is the ID of that target object
  object_id = models.PositiveIntegerField()
  # When querying data we wanna get the actual object that this tag is applied to, the actual product
  content_object = GenericForeignKey()