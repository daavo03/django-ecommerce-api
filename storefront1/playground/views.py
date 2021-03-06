from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
# Q is short for Query, using this class we can represent a query expression or a piece of code produces a value
# Also importing the Value class, Func class
from django.db.models import Q, F, Value, Func, ExpressionWrapper
from django.db.models import DecimalField
# Importing aggregate class
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
# Importing the concat class
from django.db.models.functions import Concat
# We import the ContentType model to represent the ContentType table we saw
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from store.models import Customer, Order, OrderItem, Product, Collection
from tags.models import TaggedItem


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
  #queryset = Customer.objects.annotate(new_id=F('id') + 1)


  # Calling a Database Function
  #queryset = Customer.objects.annotate(
    # Here we call the CONCAT function of a DB engine
    #New field to our customers, first name and last name. We reference fields using F objects
    #Then we need to give this a keyword argument that specifies the target function. So we set "function" to 'CONCAT'
    #Next we need to add a space in between
    #full_name = Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
  #)

  #Using the Concat class instead of Func class
  #queryset = Customer.objects.annotate(
    #full_name = Concat('first_name', Value(' '), 'last_name')
  #)


  # Grouping Data
  #See the number of orders each Customer has placed
  #queryset = Customer.objects.annotate(
    #orders_count=Count('order')
  #)


  # ExpressionWrapper
  #We gonna annotate our products and give them a new field "discounted_price"
  #queryset = Product.objects.annotate(
    #discounted_price = F('unit_price') * 0.8
  #)
  """ 
  In the query above we get an error Expression contains mixed types.
  We need to import the ExpressionWrapper class from the models module, and wrap our expression inside an
  expressionwrapper object and that's where we specify the type of the output field
  """
  #discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
  #queryset = Product.objects.annotate(
    #discounted_price = discounted_price
  #)


  # Querying Generic Relationships
  """ 
  We have the Tags app with 2 models:
    - Tag
    - TaggedItem
      - We use the ContentType framework to decouple this app from the storeapp
  
  This app knows nothing about the store app.
  
  In our DB we have a table "django_content_type" in this table we can see ALL the models we have in our application.
  In the "tags_taggeditem" we have a few column. So to find the tags for a given product:
    - We have to find the "content_type_id" of the Product model
      - In my table "django_content_type" the Product model with an id 11

  So we can write a query to filter all records where "content_type_id" equals 11. And "object_id" equals the ID of the
  product whose tags you wanna find out
  """
  #First we need to find the ContentType ID for the Product model
  #So down here we have the content type instance (the row we saw in the table with ID 11)
  #content_type = ContentType.objects.get_for_model(Product)

  #Filter tagged item
  #The actual tag is stored in the Tag table we need to preload the "tag_id" field
  #queryset = TaggedItem.objects.select_related('tag').filter(
    # We are gonna give it 2 filters
    #content_type=content_type,
    #The object id to the ID of the product whose tags we wanna query
    #object_id=1
  #)
  """ 
  In the results of the queryset we have 2 querys:
    1. Finding the Content Type ID for our Product model
    2. Reading the tags for the given product
  """


  # Custom Managers
  #Using new method to get the Tags for a given object
  #TaggedItem.objects.get_tags_for(Product, 1)


  # Caching mechanism build into querysets
  #queryset = Product.objects.all()
  #Converting the queryset to a list
  #list(queryset)
  """ 
  When we convert the queryset to a list Django evaluate the queryset and that's when it's go to the DB to get the
  result. This is expensive.

  When Django evaluates the query and gets data from DB is gonna stored it in the QuerySet Cache. The second time
  we convert the queryset to a list Django read the result from the QuerySet Cache.

  Same happens if we access an individual element from the QuerySet. Django reads this object from the QuerySet Cache.

  Note.
    Caching happens only if it evaluated the entire queryset first. 
  """


  # Inserting a record in DB
  #Create a collection object
  # collection = Collection()
  # collection.title = 'Video Games'
  # collection.featured_product = Product(pk=1)

  # #To insert this Collection to our DB using save() method
  # #In this case because we haven't set the ID of this collection Django will treat this as an insert operation
  # collection.save()

  #Another way
  #collection = Collection.objects.create(name='a', featured_product_id=1)



  # Updating objects
  #collection = Collection(pk=11)
  #collection.title = 'Games'
  #collection.featured_product = None

  #collection.save()

  #We only want to update the feature product for this collection
  #collection = Collection(pk=11)
  #collection.featured_product = None

  #collection.save()
  """ 
  Django is setting the title of the Collection to an empty string
  The collection object we have in memory by default it's title is set to an empty string. So even if it don't
  explicitly update this field Django is gonna included in our SQL statement.

  To properly update object in Django applications first we have to read it from the DB so we have all the values
  in memory then we can update it
  """
  #collection = Collection.objects.get(pk=12)
  #collection.featured_product = None
  #collection.save()

  #Avoiding the extra read
  #This update method will update the field for all objects in our queryset
  #Collection.objects.update(featured_product=None)

  # Targeting a particular collection
  #Collection.objects.filter(pk=11).update(featured_product=None)



  # Deleting an Object
  #collection = Collection(pk=11)
  #collection.delete()
  #Deleting multiple objects
  #Collection.objects.filter(id__gt=5).delete()



  # Transactions
  #Saving an order with his items
  #with transaction.atomic():
    #order = Order()
    #order.customer_id = 1
    #order.save()

    #item = OrderItem()
    #item.order = order
    # Here making the transaction fail
    #item.product_id = -1
    #item.quantity = 1
    #item.unit_price = 10
    #item.save()



  # Executing Raw SQL Queries
  queryset = Product.objects.raw('SELECT * FROM store_product')
  

  return render(request, 'hello.html', { 'name': 'Daniel', 'result': list(queryset) })