# Generated by Django 4.0.3 on 2022-04-03 06:05

# To create this empty migration python manage.py makemigrations store --empty
# Remember to go back to migration 0004 python manage.py migrate store 0004

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_customer_store_custo_last_na_e6a359_idx_and_more'),
    ]

    operations = [
        # In the constructor we can 2 sql statements: 1. Upgrading our DB, 2. Downgrading
        # For this demo we're going to insert a new record in the collection table
        #Using the same technique we can create a store procedure, function a view and so on
        migrations.RunSQL("""
            INSERT INTO store_collection (title)
            VALUES ('collection1')
        """, """
            DELETE FROM store_collection
            WHERE title='collection1'
        """)
    ]
