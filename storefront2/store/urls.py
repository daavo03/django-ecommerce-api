# Mapping the view function to URL pattern

from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.product_list),
    # Adding a parameter
    #Applying a converter to this parameter
    path('products/<int:id>/', views.product_detail),
    path('collections/', views.collection_list),
    # We can give this mapping a name which is used in the serializer argument "view_name"
    # also changing the parameter to pk
    path('collections/<int:pk>/', views.collection_detail, name='collection-detail')
]
