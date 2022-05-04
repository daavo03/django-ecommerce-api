# Mapping the view function to URL pattern

from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.product_list),
    # Adding a parameter
    #Applying a converter to this parameter
    path('products/<int:id>/', views.product_detail)
]
