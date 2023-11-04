from django.db import models
from django.contrib.auth.models import User


# shop models, related to each other (northwind like)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    desc = models.CharField(max_length=100)
    img = models.ImageField(default="../static/images/default.png")
    
    def __str__(self):
        return self.desc
    
    
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    desc = models.CharField(max_length=100)
    price = models.FloatField()
    img = models.ImageField(default="../static/images/default.png")
    ctg =models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.desc
    
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orderDate = models.DateTimeField(auto_now_add=True) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'oreder {self.id}'
    
class OrederDetails(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  
      
    def __str__(self):
        return f'order details {self.id}'
    
    
    