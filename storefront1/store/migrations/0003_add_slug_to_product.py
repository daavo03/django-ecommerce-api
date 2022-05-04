# Generated by Django 4.0.3 on 2022-04-03 03:46
# We algo give a more descriptive name

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_price_to_unit_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            # This option, this default value it's not in our model only in migration file
            # It could be used only once 
            field=models.SlugField(default='-'),
            preserve_default=False,
        ),
    ]