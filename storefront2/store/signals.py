# In Django our Models have a bunch of signals or notifications that are fired at diff times like 
#pre_save, post_save, pre_delete, post_delete so in our app we can listen to this signals and do something
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Customer

# We need to tell Django that the function should be call when a User model is saved. We pass 2 arguments to the receiver
#decorator: 1) Signal we're interested in 2) The model we're interested in
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
# This function has 2 parameters sender is the class which is sending the signal and the keyword arguments
def create_customer_for_new_user(sender, **kwargs):
  # In the keyword arguments we have a key 'created' which is a boolean, so we can check if a new model instance is created 
  if kwargs['created']:
    # If so here's where we are gonna create a customer
    #To get the instance we're gonna go to the kwargs and pick it
    Customer.objects.create(user=kwargs['instance'])