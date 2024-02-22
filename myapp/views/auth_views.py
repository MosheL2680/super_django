#####################################################
# views/routes for authentication related functions #
#####################################################

import logging
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from myapp.views.utils import log_execution_time, send_mail_receipt
from ..serializers import   MyTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import get_object_or_404


#logger config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Login - get token with payload from sirializer
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Route to create new user
@api_view(['POST', 'PUT'])
def register_or_update_user(req):
    if req.method == 'POST':
        # Create a new user
        User.objects.create_user(
            username=req.data["username"],
            password=req.data["password"],
            email=req.data["email"]
        )
        logger.info("User registered successfully") #svae info to logger
        return Response({"user": "created successfully"}, status=status.HTTP_201_CREATED)
    elif req.method == 'PUT':
        # Update an existing user
        username = req.data.get("username")
        password = req.data.get("password")
        email = req.data.get("email")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update user fields
        if password:
            user.set_password(password)
        if email:
            user.email = email

        user.save()

        return Response({"user": "updated successfully"})
     

# @Route to upd user details
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_details(request):
    print(request.data)
    user = request.user
    data = {
        'username': request.data.get('username', user.username),
        'password': request.data.get('password', user.password),
        'email': request.data.get('email', user.email),
    }
    serializer = UserSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Route to send resit password link via mail
@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')

    # Find the user with the provided email
    user = get_object_or_404(User, email=email)

    # Generate a unique token for password reset
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)

    # Create a password reset link with the token
    # reset_url = f"{request.build_absolute_uri('/')[:-1]}/password-reset-confirm/{uidb64}/{token}/"

    # Send an email to the user with the reset link
    subject = "Password Reset"
    message = f"Click the following link to reset your password: Not implemented yet"# {reset_url}"
    from_email = "noreply@example.com"  # Update with your email
    to_email = [user.email]
    
    send_mail(subject, message, from_email, to_email, fail_silently=False)

    return Response({"message": "Password reset email sent successfully"}, status=status.HTTP_200_OK)