import logging
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from myapp.views.utils import log_execution_time, send_mail_receipt
from ..models import Category, Product, Order, OrderDetail
from ..serializers import CategorySerializer, MyTokenObtainPairSerializer, OrderSerializer, ProductSerializer, UserSerializer, OrderDetailSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator

#logger config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# CheckOut - get cart from user and save it to Order and OrderDetail
@method_decorator(log_execution_time(logger, "checkOut view")) # A custom decorator that prints the time the process took
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

        OrderDetail.objects.create(order=order, product=product, quantity=quantity)

        total_price += product.price * quantity

    order.total_price = total_price
    order.save()
    # Call the helper function to send email
    try:
        send_mail_receipt(user, cart_data, total_price)
    except Exception as e:
        return Response({"error": f"An error occurred while sending the email: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    logger.info("Order saved successfully")
    return Response("order saved fucking successfuly", status=status.HTTP_201_CREATED)


# Route to get user's orders history
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    
    orders_data = []
    
    for order in orders:
        order_details = OrderDetail.objects.filter(order=order)
        order_data = {
            "order_id": order.id,
            "order_date": order.orderDate,
            "order_details": []
        }

        for detail in order_details:
            product = Product.objects.get(id=detail.product.id)
            product_data = {
                "product_id":product.id,
                "product_desc": product.desc,
                "product_price": product.price,
                "quantity": detail.quantity,
                "product_image": product.img.url if product.img else ''  # Check and access the image URL field
            }
            order_data["order_details"].append(product_data)

        orders_data.append(order_data)

    user_data = {"username": user.username,"email": user.email,}
    
    response_data = {"user": user_data,"orders": orders_data }

    return Response(response_data)

# Full CRUD using serializer for product & categoy models. 
# not really needed for now because i'm using "/admin"
class ProductsView(APIView):
    # permission_classes = [IsAuthenticated, IsAdminPermission] #Make sure user is admin

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
        else:
            errors = {
                'error': 'Validation failed',
                'details': serializer.errors
            }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"error": f"Product not found with id {id}"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({"error": f"Product not found with id {id}"})
        
        product.delete()
        return Response({"message": "Deleted successfully"})


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