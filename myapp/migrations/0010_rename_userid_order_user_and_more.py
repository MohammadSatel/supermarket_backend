# Generated by Django 4.2.6 on 2023-11-03 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_rename_orders_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='userID',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='orederdetails',
            old_name='orderID',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='orederdetails',
            old_name='productID',
            new_name='product',
        ),
    ]