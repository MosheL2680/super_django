from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register', views.register),
    path('login/', views.MyTokenObtainPairView.as_view()),
    path('logout/', auth_views.LogoutView.as_view()),
    path('products/', views.ProductsView.as_view()),
    path('categories', views.CategoriesView.as_view()),
    path('checkout', views.checkOut),
    path('products/<int:catID>', views.ProductsView.as_view()),
    path('history', views.get_orders),
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
