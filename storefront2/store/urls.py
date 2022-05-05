# Mapping the view function to URL pattern

from django.urls import path
from . import views

# URLConf
urlpatterns = [
    # In order to use view class need to use as_view() method which will convert the class to a regular function based view
    path('products/', views.ProductList.as_view()),
    # Adding a parameter
    #Applying a converter to this parameter
    path('products/<int:id>/', views.ProductDetail.as_view()),
    path('collections/', views.CollectionList.as_view()),
    # We can give this mapping a name which is used in the serializer argument "view_name"
    # also changing the parameter to pk
    path('collections/<int:pk>/', views.collection_detail, name='collection-detail')
]
