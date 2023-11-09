from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Category, Product, Order, OrederDetail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
    def create(self, validated_data):
        user = self.context['user']
        print(user)
        return Order.objects.create(**validated_data,user=user)
    
    
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrederDetail
        fields = '__all__'
        
        

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom columns (user return payload - when login )
        token['username'] = user.username
        return token