import os
from celery import Celery

# Setting env variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')

# Creating Celery instance
celery = Celery('storefront')
# Where celery can find configuration variables
celery.config_from_object('django.conf:settings', namespace='CELERY')
# We'll create a task and that task it's gonna be in the tasks module so here we're instructing celery to auto discover
#all this tasks
celery.autodiscover_tasks()