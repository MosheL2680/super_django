from django.contrib import admin
from .models import Category, Product, Order, OrederDetails

# Register your models here.
admin.site.register([Category, Product, Order, OrederDetails])