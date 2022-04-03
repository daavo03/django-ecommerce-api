from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product

def say_hello(request):
  # Every model in django has an attribute called ".objects", this return a manager object (interface to DB)
  #Most of the methods return a queryset (object that encapsulate a query). At some point django will evaluate the
  #query and django will generate the right SQL statement to sent to our DB. This will happen under a few scenarios
  query_set = Product.objects.all()

  # One scenario when we iterate over a queryset
  #for product in query_set:
    #print(product)

  # When we convert it to a list
  #list(query_set)

  # When we access an individual element or slice
  #query_set[0:5]

  # We can use query_set methods to build complex querys
  # To filter the results, will return a new query set, we can chain it to call a 2nd filter method, also use the order_by
  #method to sort the result
  #query_set.filter().filter().order_by()


  return render(request, 'hello.html', { 'name': 'Daniel' })