# Generated by Django 4.0.3 on 2022-05-03 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_remove_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='is_active',
        ),
    ]
