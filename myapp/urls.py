from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register', views.register),
    path('login/', TokenObtainPairView.as_view()),
    path('products', views.ProductsView.as_view()),
    path('checkout', views.checkOut),
    path('products/<int:id>', views.ProductsView.as_view()),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
