# Generated by Django 4.2.6 on 2023-11-01 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_rename_description_category_desc_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='ctg',
        ),
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(default='products/default.jpg', upload_to='products/'),
        ),
    ]