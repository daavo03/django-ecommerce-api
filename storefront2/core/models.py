from django.contrib.auth.models import AbstractUser
from django.db import models

# In the Core APP we combine features from diff apps. Code written in the Core app is specific to this project. So here
#we can add our Custom User Model


# Here we extend the User Model creating new Model extending AbstractUser class in the authentication system
class User(AbstractUser):
  # Redefining email field
  email = models.EmailField(unique=True)