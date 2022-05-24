# Mapping the view function to URL pattern

from django.urls import path
from django.urls.conf import include
# Now we'll use the router that comes with nested 
from rest_framework_nested import routers
from . import views


# Creating router object
# If we use DeafultRouter we get 2 additional features. 1) basic root view in localhost/store, 2) getting data in json adding .json of route
#router = SimpleRouter()
router = routers.DefaultRouter()
# Register our viewsets with this router object. We'll be saying that the products endpoint should be manage by the ProductViewSet 
#Passing 2 arguments: 1. Prefix value we're using as the name of our endpoint "products", 2. Our viewset
#Explicitly specifying the basename bc we have a method for the queryset in the ProductViewSet
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
# Registering new end point for the cart
router.register('carts', views.CartsViewSet)
router.register('customers', views.CustomerViewSet)
# Registering new end point for orders
# Because we remove the "queryset" attribute from the OrderViewSet and we're overwriting the get_queryset(),
#Django rest framework cannot figure out the basename for our endpoint, so we set the basename for this endpoint for generating the name of views 
router.register('orders', views.OrderViewSet, basename='orders')

# Creating nested default router
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
# Registering the child resources. The basename is used to generate the name of our urlpatterns
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

# Creating nested router for the cartItems
#Once we set the lookup to "cart" we have a URL paramter called "cart_pk" that's how we extract the URL paramter from the
#overwrote queryset
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
# On this router we register a new endpoint and map it to views of "CartItemViewSet"
carts_router.register('items', views.CartItemViewSet, basename='cart-items')


"""
# URLConf
urlpatterns = [
    # In order to use view class need to use as_view() method which will convert the class to a regular function based view
    path('products/', views.ProductList.as_view()),
    # Adding a parameter
    #Applying a converter to this parameter
    # Our generic view expects the parameter ID to be called PK, so we change it
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('collections/', views.CollectionList.as_view()),
    # We can give this mapping a name which is used in the serializer argument "view_name"
    # also changing the parameter to pk
    path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail')
]
"""

# URLConf
# If we don't have explicit patterns
# Combining the urls of both routers and include them in the url pattern object
# Including the new routers urls in the url patterns list
urlpatterns = router.urls + products_router.urls + carts_router.urls
""" 
# If we have some specific patterns in the array
urlpatterns = [
    # For route it's an empty string, and we're gonna include() and with it we can import routes from somewhere else
    path('', include(router.urls))
] 
"""