# Generated by Django 4.2.5 on 2023-10-03 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cartitems_variation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitems',
            old_name='variation',
            new_name='variations',
        ),
    ]
