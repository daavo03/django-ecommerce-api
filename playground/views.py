from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
# Q is short for Query, using this class we can represent a query expression or a piece of code produces a value
from django.db.models import Q, F
from store.models import OrderItem, Product

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

  # Find the products whose price is in a given range
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
  #queryset = Product.objects.filter(description__isnull=True)

  # Apply multiple filters
  #Find all products with inventory < 10 AND price < 20
  #one way pass multiple keyword arguments
  #queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
  #Chain the call to filter()
  #queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)

  #Combine conditions using OR operator
  #We have to use Q objects, using Q class we can encapsulate a keyword argument
  #queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
  #We can also use the AND operator
  #queryset = Product.objects.filter(Q(inventory__lt=10) & Q(unit_price__lt=20))
  #Negate a Q object
  #Get all products whose inventory is less than 10 AND their unit price IS NOT less than 20
  #queryset = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))

  # Filtering data we need to reference a particular field
  #find all products where the inventory = price
  #queryset = Product.objects.filter(inventory=F('unit_price')) #WHERE `store_product`.`inventory` = (`store_product`.`unit_price`)
  #Using f objects we can also reference a field in a related table
  #queryset = Product.objects.filter(inventory=F('collection__id')) # WHERE `store_product`.`inventory` = (`store_product`.`collection_id`)

  # Sorting data
  #Using the order_by() method we can sort the results by 1 or more fields
  #Getting al the products and sort them by their title in ASC
  #queryset = Product.objects.order_by('title')
  # Changing the sort direction
  #queryset = Product.objects.order_by('-title')
  # Sort by multiple fields
  #queryset = Product.objects.order_by('unit_price', '-title')
  # The order_by returns query_set object and 1 of the methods is reverse, if we call it will reverse the direction of the sort
  #queryset = Product.objects.order_by('unit_price', '-title').reverse()
  # We can also call the order_by() after filtering data
  #queryset = Product.objects.filter(collection__id=1).order_by('unit_price')

  # Sort and pick 1st object 
  #with this implementation we're not going to get a queryset because we're accessing an individual element
  #the moment we access an individual element in the queryset, the queryset gets evaluated and then we get an actual object
  #product = Product.objects.order_by('unit_price')[0]
  # Rewriting same query
  #the earliest() method returns an object
  #product = Product.objects.earliest('unit_price')
  #similarly we have latest() sorts the products by unit_price in descending order and return the 1st object
  #product = Product.objects.latest('unit_price')

  # Limiting results
  #we wanna show 5 products per page, to do that we use python array slicing syntax
  #Returning the first 5 objects in this array
  #queryset = Product.objects.all()[:5]
  #Get the products on the 2nd page
  #queryset = Product.objects.all()[5:10]

  # Selecting specific fields
  #queryset = Product.objects.values('id','title') #SELECT `store_product`.`id`, `store_product`.`title` FROM `store_product
  #Reading related fields
  #queryset = Product.objects.values('id','title', 'collection__title')
  """
  With this implementation we have an inner join between the Product and the Collection tables because we're
  reading a related field

  SELECT `store_product`.`id`,
         `store_product`.`title`,
         `store_collection`.`title`
  FROM `store_product`
  INNER JOIN `store_collection`
    ON (`store_product`.`collection_id` = `store_collection`.`id`)

  With this method instead of getting a bunch of product instances, we get a bunch of dictionary objects.
  In the HTML:
    {'id': 2, 'title': 'Island Oasis - Raspberry', 'collection__title': 'Beauty'}
    {'id': 3, 'title': 'Shrimp - 21/25, Peel And Deviened', 'collection__title': 'Beauty'}
    .
    ..
    ...

  Each object in the result it's a dictionary
  """
  #Method values_list() we get tuples instead of dictionaries
  #queryset = Product.objects.values_list('id','title', 'collection__title') 
  """ 
  (2, 'Island Oasis - Raspberry', 'Beauty') 
  (3, 'Shrimp - 21/25, Peel And Deviened', 'Beauty')
  .
  ..
  ...

  Each object is a tuple of 3 values
  """
  #Selecting products that have been ordered and sorting them by title
  queryset =  Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
  """ 
  We should start with the "OrderItem" table. 
  So we import the "OrderItem" class at the top
  Now in this table we need to select all the product ids from this table. Here we use the values() or values_list() method
  Once we have selected the "product_id" we store the results in a variable "queryset"
    queryset = OrderItem.objects.values('product_id') # {'product_id': 1}

  To get rid of duplicates we can use the distinct() method
    queryset = OrderItem.objects.values('product_id').distinct()

  Now we want to go to the Product table and select all products with the ids selected above.
  So we'll be using the __in lookup type to find all products whose ID is in the given list
  And we're going to set the expression to the selected product_id from the OrderItem table:
    Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct())
  We set it now to the queryset:
    queryset = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct())

  Now let's sort the list
  We'll call the order_by()
    queryset = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
  """
  




  return render(request, 'hello.html', { 'name': 'Daniel', 'products': list(queryset) })