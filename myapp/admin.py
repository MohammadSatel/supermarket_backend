from django.contrib import admin
from .models import Category, Product, Order, OrderDetail

# Register models.
admin.site.register([Category, Product, Order, OrderDetail])