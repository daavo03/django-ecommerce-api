from turtle import title
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product

def say_hello(request):
  # Every model in django has an attribute called ".objects", this return a manager object (interface to DB)
  #Most of the methods return a queryset (object that encapsulate a query). At some point django will evaluate the
  #query and django will generate the right SQL statement to sent to our DB. This will happen under a few scenarios
  #query_set = Product.objects.all()

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

  # Methods for retrieving objects
  #all()  When it's evaluated we get all the objects in a given table
  #queryset = Product.objects.all()
  #get()     Getting a single object
  #product = Product.objects.get(id=1) #pk=1 when using pk django will auto translate this to the name of the PK field
  #if it cannot find this object it will throw an exception, to handle this wrap code inside try/catch
  #try:
    #product = Product.objects.get(pk=0)
  #except ObjectDoesNotExist:
    #pass

  #Better way to try-catch
  #The filter() method returns a queryset, so rightaway we can call the first() method of the queryset
  #if the queryset is empty the first() returns none. So in this case "product" is going to be none
  #product2 = Product.objects.filter(pk=0).first()

  #Check the existence of an object
  #We get a boolean value
  #exists = Product.objects.filter(pk=0).exists()

  # Let's say we want to find all the products that are 20 dollars
  #queryset = Product.objects.filter(unit_price=20)
  
  # Find all the products that are more expensive than 20 dollars
  #using filter() we need to pass keyword=value
  #queryset = Product.objects.filter(unit_price__gt=20)

  # Find the prodcuts whose price is in a given range
  #queryset = Product.objects.filter(unit_price__range=(20, 30))

  # Filter across relationships
  #find all the products in collection 1
  #queryset = Product.objects.filter(collection__id__range=(1,2,3))

  # Find products contains coffee in their tittle
  #contains this lookup type is case sensitive
  #to perform case insensitive search use "icontains"
  #queryset = Product.objects.filter(title__icontains='coffee')

  # For dates
  #All products updated in 2021
  #queryset = Product.objects.filter(last_update__year=2021)
  #compare with a date value
  #queryset = Product.objects.filter(last_update__date=2021)

  # Checking for null
  #To get all the products without a description
  queryset = Product.objects.filter(description__isnull=True)






  return render(request, 'hello.html', { 'name': 'Daniel', 'products': list(queryset) })