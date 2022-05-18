from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

# If we want to add fields as part of registration we use a Custom Serializer
class UserCreateSerializer(BaseUserCreateSerializer):
  # We want this Meta class to inherit everything in the Meta class of the "BaseUserCreateSerializer" class
  class Meta(BaseUserCreateSerializer.Meta):
    # We only overwrite fields attribute
    fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']  
