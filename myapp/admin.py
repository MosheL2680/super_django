from django.contrib import admin
from .models import Category, Product, Order, OrderDetail

# Register your models here.
admin.site.register([Category, Product, Order, OrderDetail])