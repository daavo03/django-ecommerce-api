from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
# Q is short for Query, using this class we can represent a query expression or a piece of code produces a value
# Also importing the Value class
from django.db.models import Q, F, Value
# Importing aggregate class
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from store.models import Customer, Order, OrderItem, Product

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
  #queryset =  Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
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
  

  # Deferring fields
  #We have only() method we can specify the fields we want to read from the DB
  #queryset = Product.objects.only('id', 'title')
  """ 
  With the only() method we'll get instances of the product class
  With the values() method we'll get dictionary objects

  Careful with this method we can end up with a long of queries send to the DB under the hood
  If we also render the price of each product in the HTML, when we reload the page it take a lot until we see results

  In the SQL tab we have 1003 queries.
  We have a main query where we read the ID and title from the product table
  After the main query FOR EACH PRODUCT we have a separate query to read it's price
  Because we have 1000 products in this list, we have 1000 extra queries for reading the price of all this products
  """
  #defer() Method we can defer the loading of certain fields to later
  #queryset = Product.objects.defer('description')

  # Preload bunch of objects together - Products with their Collection
  #queryset = Product.objects.select_related('collection').all()
  """ 
  The query of what's happening:

  SELECT `store_product`.`id`,
         `store_product`.`title`,
         `store_product`.`slug`,
         `store_product`.`description`,
         `store_product`.`unit_price`,
         `store_product`.`inventory`,
         `store_product`.`last_update`,
         `store_product`.`collection_id`,
         `store_collection`.`id`,
         `store_collection`.`title`,
         `store_collection`.`featured_product_id`
  FROM `store_product`
  INNER JOIN `store_collection`
    ON (`store_product`.`collection_id` = `store_collection`.`id`)

  When we use this method django creates a join between our table
  Also we use it when the other end of the R.S has 1 instances like in this case a product has 1 collection.

  We use prefetch_related() when the other end of the R.S has many objects. An example is the promotions of a product
  """


  # Span Relationships
  #Collection has another field that we want to preload as part of this query
  #queryset = Product.objects.select_related('collection__someOtherField').all()
  #Preload promotions
  #queryset = Product.objects.prefetch_related('promotions').all()
  """ 
  Watching the query we have 2 querys:

  SELECT `store_product`.`id`,
       `store_product`.`title`,
       `store_product`.`slug`,
       `store_product`.`description`,
       `store_product`.`unit_price`,
       `store_product`.`inventory`,
       `store_product`.`last_update`,
       `store_product`.`collection_id`
  FROM `store_product`

  We have another query to read the promotions of these products.

  SELECT (`store_product_promotions`.`product_id`) AS `_prefetch_related_val_product_id`,
       `store_promotion`.`id`,
       `store_promotion`.`description`,
       `store_promotion`.`discount`
  FROM `store_promotion`
  INNER JOIN `store_product_promotions`
    ON (`store_promotion`.`id` = `store_product_promotions`.`promotion_id`)
  WHERE `store_product_promotions`.`product_id` IN (1, 2, 3, 4, 5, 6,...,)

  So we're reading 3 columns from the promotion table and we have a join between promotion and product

  Basically we have 2 results set
  """
  # We can also combine the 2 methods
  #We want to load all the products with their promotions and collection
  #Both of the methods return a queryset, order doesn't matter
  #queryset = Product.objects.prefetch_related('promotions').select_related('collection').all()

  # Get the last 5 orders with their customers and items (including product referencing each orderitem)
  """ 
  We want to get a list of orders. So we should start with the Order class then we go to objects, now we want to
  preload this orders with their customer, so this is where we call "select_related()" to preload the 'customer' field
    Order.objects.select_related('customer)
  
  Now, we don't show all the orders we wanna show the last 5 orders, so we need to sort them by "placed_at" by desc
  and then we use array slicing syntax to pick the top 5 orders:
    Order.objects.select_related('customer).order_by('-placed_at')[:5]
  """
  #queryset = Order.objects.select_related('customer').order_by('-placed_at')[:5]
  """ 
  Let's look our SQL tab 

  SELECT `store_order`.`id`,
         `store_order`.`placed_at`,
         `store_order`.`customer_id`,
         `store_order`.`payment_status`,
         `store_customer`.`id`,
         `store_customer`.`first_name`,
         `store_customer`.`last_name`,
         `store_customer`.`email`,
         `store_customer`.`phone`,
         `store_customer`.`birth_date`,
         `store_customer`.`membership`
  FROM `store_order`
  INNER JOIN `store_customer`
    ON (`store_order`.`customer_id` = `store_customer`.`id`)
  ORDER BY `store_order`.`placed_at` DESC
  LIMIT 5

  We have a single query to read the orders and their customer. 
  So we're selecting all the columns from the order table and all the columns from the customer table.
  THen we have a join between order and customer tables

  Now we should preload the items of these orders.
  So we call prefetch_related(), because each order can have many items. The name of the field we're gonna query
  in the Order class we have 3 fields we don't have a field called "items". But look at the "OrderItem" class there
  we have "order" which is a F.K to "Order" class, so django will create the reverse R.S for us the name of that R.S
  is "orderitem_set"
  So we wanna prefetch "orderitem_set":
    queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set').order_by('-placed_at')[:5]
  """
  #queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set').order_by('-placed_at')[:5]
  """ 
  Last step is to load the product referrencing each orderItem.
  """
  #queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]


  # Count our Products 
  #If we use 'id' count total number products, bc every product has an ID. Proper way to count (or using P.K field) 
  #If we use f.e. 'description' and assuming description can be null. It will count the number of products that have a
  #description
  #aggregate() method doesn't return a query set
  #result = Product.objects.aggregate(Count('id')) #We got a dictionary with one k-v pair: {'id__count': 1000}

  #Changing the name of the key
  #result = Product.objects.aggregate(count = Count('id')) # {'count': 1000}

  #Calculate multiple summaries. 
  #The minimum price of our products
  #result = Product.objects.aggregate(count = Count('id'), min_price = Min('unit_price')) # {'count': 1000, 'min_price': Decimal('1.06')}
  
  #We can filter our products in a given collection and then calculate the summaries over that dataset
  #result = Product.objects.filter(collection__id=1).aggregate(count = Count('id'), min_price = Min('unit_price')) 

  
  # Add additional attributes to objects while querying
  #Let's say while querying customers we wanna give each Customer a new field called "is_new=True"
  #queryset = Customer.objects.annotate(is_new=True)
  """ 
  But we got an error we cannot pass a Boolean value we need to pass an expression object.

  In Django we have the Expression class which is the base class for all types of expressions. Derivaties of this class 
  are:
    - Value
      - Representing single values like a number, boolean, string
    - F
      - Reference a field in the same or in other table
    - Func
      - Calling database functions
    - Aggregate
      - Based class for all aggregate classes Count, Sum, Max, Min, etc
  """
  #Passing an Expression Object
  #queryset = Customer.objects.annotate(is_new=Value(True)) #In the list of Customers we got new column "IS_NEW" set to 1

  #Giving our Customers new field called "new_id" set it to the same value as the ID field.
  #So we need to reference another field in this model
  #queryset = Customer.objects.annotate(new_id=F('id'))

  #Also perform computations
  #Add +1 to the NEW_ID
  queryset = Customer.objects.annotate(new_id=F('id') + 1)



  return render(request, 'hello.html', { 'name': 'Daniel', 'result': list(queryset) })