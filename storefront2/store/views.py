from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
# Here we should create a view function (take a request returns a response)
def product_list(request):
  # Here we return a response object
  return Response('ok')

# Create another view function for seeing details of a product
@api_view()
#Giving the id parameter
def product_detail(request, id):
  # Returning the id in the response verify all works
  return Response(id)