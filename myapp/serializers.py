from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Category, Product, Order, OrederDetail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User


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
        token['username'] = user.username
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # Custom logic for creating a user, if needed
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Custom logic for updating a user, if needed
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        
        # Handle password separately to ensure proper hashing
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance
