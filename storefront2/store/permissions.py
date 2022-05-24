from rest_framework import permissions

# Creating custom permission class
class IsAdminOrReadOnly(permissions.BasePermission):
  # We overwrite the "has_permission"
  def has_permission(self, request, view):
      # Anyone can access the target view 
      # With implementation above even HEAD or OPTION requests require the user to be an admin
      #if request.method == 'GET': 
      # Better way to write the condition we can check to see if the method is in the list of save request methods
      if request.method in permissions.SAFE_METHODS:
        return True
      # Otherwise return true if both conditions True
      return bool(request.user and request.user.is_staff)


# Preventing people outside the "Customer Service" group viewing data and extend the Django Model permissions
class FullDJangoModelPermissions(permissions.DjangoModelPermissions):
  # Defining a constructor
  def __init__(self) -> None:
      # To send the GET request, the user should have the view permission
      self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']