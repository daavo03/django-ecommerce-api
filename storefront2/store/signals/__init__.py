# Every time we receive an order in the store app like order created with this other apps interested in this event 
#can subscribe to this signal and get notified

# Here we define our signals

from django.dispatch import Signal

order_created = Signal()