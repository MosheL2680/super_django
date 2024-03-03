############################################################################################
# This file contains helper functions that i'm using in the "views" and "auth_views" files #
############################################################################################

import logging
import time
from django.core.mail import send_mail
from rest_framework.permissions import BasePermission
import implicit
import pandas as pd
from scipy.sparse import coo_matrix
from ..models import Order, OrderDetail


# Helper function for product recommendations
def suggest_products(user_id):
    # Load order data
    orders = Order.objects.filter(user=user_id)

    data = []
    for order in orders:
        order_details = OrderDetail.objects.filter(order=order)
        for detail in order_details:
            data.append({'user': user_id, 'item': detail.product.id})  # No explicit rating needed

    # Create a user-item matrix
    df = pd.DataFrame(data)
    df['value'] = 1  # Add a column for the ratings (1 for interaction)
    user_item_matrix = coo_matrix((df['value'], (df['user'], df['item'])))



    # Use implicit for collaborative filtering
    model = implicit.als.AlternatingLeastSquares(factors=50, regularization=0.1, iterations=50)
    model.fit(user_item_matrix.T)

    # Get user's product interactions
    user_interactions = user_item_matrix.T.tocsr()[user_id]

    # Recommend products
    recommended_products = model.recommend(user_id, user_item_matrix, N=5, filter_already_liked_items=False)

    # Check if recommended_products is a tuple, and convert it to a list
    if isinstance(recommended_products, tuple):
        recommended_products = list(zip(recommended_products[0], recommended_products[1]))

    # Return only product IDs
    return [product_id for product_id, _ in recommended_products]




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