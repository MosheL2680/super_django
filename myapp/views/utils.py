############################################################################################
# This file contains helper functions that i'm using in the "views" and "auth_views" files #
############################################################################################

import logging
import time
from django.core.mail import send_mail
from rest_framework.permissions import BasePermission

# A decorator that check how much time the function tooks
def log_execution_time(logger, message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.info(f"{message} - Execution time: {elapsed_time:.2f} seconds")
            return result
        return wrapper
    return decorator


# Helper function to send mail receipt
def send_mail_receipt(user, user_cart, total_price):
    subject = f"Your Receipt, {user}"

    # Format the products in a nice way
    products_info = ""
    for product in user_cart:
        products_info += f"\n- {product['amount']} x {product['desc']} (${product['price']} each)"

    message = f"Thank you for your order! Here is the summary:\n\nYou ordered:{products_info}\n\nTotal payment: ${total_price}"

    send_mail(
        subject,
        message,
        "mosheshop.super@gmail.com",
        [user.email],
        fail_silently=False,
    )
    
#  Verify if admin (permission check)
class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has admin privileges
        return request.user and request.user.is_staff