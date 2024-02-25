from django.contrib import admin
from django.urls import path
from .views import views
from django.contrib.auth import views as authViews
from django.conf import settings
from django.conf.urls.static import static
from .views import views, auth_views


urlpatterns = [
    path('register', auth_views.register),
    path('login/', auth_views.MyTokenObtainPairView.as_view()),
    path('logout/', authViews.LogoutView.as_view()),
    path('forgotpass', auth_views.forgot_password, name='forgot_password'),
    path('products/', views.ProductsView.as_view()),
    path('categories', views.CategoriesView.as_view()),
    path('checkout', views.checkOut),
    path('products/<int:catID>', views.ProductsView.as_view()),
    path('products/delete/<int:id>', views.ProductsView.as_view()),
    path('products/update/<int:id>', views.ProductsView.as_view()),
    path('history', views.get_orders),
    path('upduser', auth_views.update_user_details),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
