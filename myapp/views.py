from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product, Order, OrederDetails
from .serializers import CategorySerializer, ProductSerializer, OrderDetailsSerializer, OrderSerializer


# Register - get username & pass and create new user
@api_view(['POST'])
def register(req):
    User.objects.create_user(username=req.data["username"], password=req.data["password"])
    return Response({"user":"created successfuly"})


# Get cart and save it in 'Order' and 'OrderDetails' models
@api_view(['POST'])
@permission_classes([IsAuthenticated])#requires authentication
def checkOut(req):
    user = req.user#gets the specific user sending the request
    cart_data = req.data.get('cart')#get the cart sent in the request body
    order = Order.objects.create(user=user, total_price=0)#create new order
    total_price = 0
    for item in cart_data:
        product_id = item['id']
        quantity = item['amount']
        product = Product.objects.get(id=product_id)#get the specific prd from pruduct model
        OrederDetails.objects.create(order=order, product=product, quantity=quantity)#create new line in 'orderDetails'
        total_price += product.price * quantity#calc total price of the cart
        order.total_price = total_price
        order.save()#save total price to order (*in 'Order' model*)
    return Response("order saved fucking successfuly")



# Full CRUD using serializer for product & categoy models. 
# not really needed for now because i'm using "/admin"

class CategoriesView(APIView):
    def get(self, request):
        # Retrieve all categories
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data)

    def post(self, request):
        # Create a new category
        category_serializer = CategorySerializer(data=request.data)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(category_serializer.data, status=status.HTTP_201_CREATED)
        return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # Update an existing category
        category = Category.objects.get(pk=request.data['id'])
        category_serializer = CategorySerializer(category, data=request.data, partial=True)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(category_serializer.data, status=status.HTTP_200_OK)
        return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Delete a category by ID
        try:
            category = Category.objects.get(pk=request.data['id'])
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)


class ProductsView(APIView):
    def get(self, request, id=None):
        if id is not None:
            try:
                product = Product.objects.get(id=id)
                serializer = ProductSerializer(product)
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
    def put(self, request):
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    def delete(self, request):
        product = Product.objects.get(id=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)