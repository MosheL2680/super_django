from rest_framework.serializers import ModelSerializer
from .models import Category, Product, Order, OrederDetails


# serializers for my 4 models

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class OrderDetailsSerializer(ModelSerializer):
    class Meta:
        model = OrederDetails
        fields = '__all__'