from django.contrib import admin
from .models import Category, Product, Order, OrederDetail

# Register your models here.
admin.site.register([Category, Product, Order, OrederDetail])