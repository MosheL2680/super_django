from decimal import Decimal
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product, Order, OrederDetail
from .serializers import CategorySerializer, MyTokenObtainPairSerializer, ProductSerializer
from rest_framework_simplejwt.views import TokenObtainPairView




# Login - get token with payload from sirializer
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Register - get username & pass and create new user
@api_view(['POST'])
def register(req):
    User.objects.create_user(username=req.data["username"], password=req.data["password"], email=req.data["email"])
    return Response({"user":"created successfuly"})


# get cart from user and save it to Order and OrderDetail
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkOut(req):
    user = req.user

    # Validate the cart data in the request
    cart_data = req.data.get('cart')
    if cart_data == []:
        return Response("cant save empty cart")
    if not isinstance(cart_data, list) or not all(isinstance(item, dict) and 'id' in item and 'amount' in item for item in cart_data):
        return Response("Invalid cart data. Expect an array of items with 'id' and 'amount' fields.", status=status.HTTP_400_BAD_REQUEST)

    order = Order.objects.create(user=user, total_price=0)

    total_price = 0
    for item in cart_data:
        product_id = item['id']
        quantity = item['amount']

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(f"Product with ID {product_id} does not exist.", status=status.HTTP_400_BAD_REQUEST)

        if quantity <= 0:
            return Response("Invalid quantity. Quantity must be greater than 0.", status=status.HTTP_400_BAD_REQUEST)

        OrederDetail.objects.create(order=order, product=product, quantity=quantity)

        total_price += product.price * quantity

    order.total_price = total_price
    order.save()

    return Response("order saved fucking successfuly", status=status.HTTP_201_CREATED)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    
    orders_data = []
    
    for order in orders:
        order_details = OrederDetail.objects.filter(order=order)
        order_data = {
            "order_id": order.id,
            "order_date": order.orderDate,
            "order_details": []
        }

        for detail in order_details:
            product = Product.objects.get(id=detail.product.id)
            product_data = {
                "product_desc": product.desc,
                "quantity": detail.quantity,
                "product_image": product.img.url if product.img else ''  # Check and access the image URL field
            }
            order_data["order_details"].append(product_data)

        orders_data.append(order_data)

    user_data = {
        "username": user.username,
        "email": user.email,
    }
    
    response_data = {
        "user": user_data,
        "orders": orders_data
    }

    return Response(response_data)



# Full CRUD using serializer for product & categoy models. 
# not really needed for now because i'm using "/admin"

class ProductsView(APIView):
    def get(self, request, catID=None):
        if catID is not None:
            try:
                products = Product.objects.filter(ctg=catID)
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)        
            return Response(serializer.data)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def put(self, request):
    #     product = Product.objects.get(id=id)
    #     serializer = ProductSerializer(product, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    # def delete(self, request):
    #     product = Product.objects.get(id=id)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class CategoriesView(APIView):
    def get(self, request):
        # Retrieve all categories
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data)

#     def post(self, request):
#         # Create a new category
#         category_serializer = CategorySerializer(data=request.data)
#         if category_serializer.is_valid():
#             category_serializer.save()
#             return Response(category_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request):
    #     # Update an existing category
    #     category = Category.objects.get(pk=request.data['id'])
    #     category_serializer = CategorySerializer(category, data=request.data, partial=True)
    #     if category_serializer.is_valid():
    #         category_serializer.save()
    #         return Response(category_serializer.data, status=status.HTTP_200_OK)
    #     return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request):
#         # Delete a category by ID
#         try:
#             category = Category.objects.get(pk=request.data['id'])
#             category.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Category.DoesNotExist:
#             return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)


