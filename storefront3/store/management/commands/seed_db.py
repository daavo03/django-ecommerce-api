from django.core.management.base import BaseCommand
from django.db import connection
from pathlib import Path
import os


class Command(BaseCommand):
    help = 'Populates the database with collections and products'

    def handle(self, *args, **options):
        print('Populating the database...')
        current_dir = os.path.dirname(__file__)
        # Full path to the sql file
        file_path = os.path.join(current_dir, 'seed.sql')
        # Using path class we read the entire text in this file 
        sql = Path(file_path).read_text()

        # Opening a connection with our DB
        with connection.cursor() as cursor:
            # Executing the sql statement
            cursor.execute(sql)
