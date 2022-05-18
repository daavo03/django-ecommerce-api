from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer

# If we want to add fields as part of registration we use a Custom Serializer
class UserCreateSerializer(BaseUserCreateSerializer):
  # We want this Meta class to inherit everything in the Meta class of the "BaseUserCreateSerializer" class
  class Meta(BaseUserCreateSerializer.Meta):
    # We only overwrite fields attribute
    fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']  

# Creating Custom Serializer to include first and last name in the /me
class UserSerializer(BaseUserSerializer):
  class Meta(BaseUserSerializer.Meta):
    fields = ['id', 'username', 'email', 'first_name', 'last_name']
