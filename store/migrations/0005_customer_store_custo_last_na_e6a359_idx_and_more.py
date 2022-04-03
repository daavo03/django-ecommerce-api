# Generated by Django 4.0.3 on 2022-04-03 04:56

# This migrations was only for teaching purposes go back to other migration 
# Remember to go back to migration 0004 python manage.py migrate store 0004

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_add_zip_to_address'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['last_name', 'first_name'], name='store_custo_last_na_e6a359_idx'),
        ),
        migrations.AlterModelTable(
            name='customer',
            table='store_customers',
        ),
    ]
