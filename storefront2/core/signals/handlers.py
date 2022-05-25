# Here in the Core app we can receive the signals
# So in our current implementation the Store app fires an "order_created" event and the Core app simply gets the order
#and prints it in the terminal, but the Store app doesn't care about what happens in the Core app after the order is created
#similarly we can have many other apps that are interested in this event like "Shipping" app and every time an order is 
#created those apps will get notified and do something that's relevant in their domain

from django.dispatch import receiver
from store.signals import order_created

# Defining the handler function with a receiver decorator receiving the signal of "order_created"
@receiver(order_created)
def on_order_created(sender, **kwargs):
  # The order is what we receive from this signal
  print(kwargs['order'])
