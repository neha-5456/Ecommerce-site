# Generated by Django 4.2.5 on 2023-10-03 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_variant'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Variant',
            new_name='variation',
        ),
    ]
