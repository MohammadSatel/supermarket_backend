# Import Django's function to create URL patterns and admin functionality
from django.contrib import admin
from django.urls import path

# Import your custom views from the current package
from . import views

# Import Django's built-in auth views for logout functionality
from django.contrib.auth import views as auth_views

# Import settings and static files serving utilities from Django
from django.conf import settings
from django.conf.urls.static import static

# Define URL patterns for your Django application
urlpatterns = [
    # URL pattern for user registration or update, calling the custom view 'register_or_update_user'
    path('register/', views.register_or_update_user, name='register'),

    # URL pattern for user login, utilizing a custom token-based view for authentication
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),

    # URL pattern for user logout, using Django's built-in LogoutView
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # URL pattern for password reset functionality, calling the custom view 'forgot_password'
    path('forgot-password/', views.forgot_password, name='forgot_password'),

    # URL pattern for viewing products, mapped to a class-based view
    path('products/', views.ProductsView.as_view(), name='product_list'),

    # URL pattern for viewing categories, mapped to a class-based view
    path('categories/', views.CategoriesView.as_view(), name='category_list'),

    # URL pattern for checkout process, calling the custom view 'checkOut'
    path('checkout/', views.checkOut, name='checkout'),

    # URL pattern for viewing products by category ID, utilizing the same 'ProductsView' with a parameter
    path('products/<int:catID>/', views.ProductsView.as_view(), name='product_by_category'),

    # URL pattern for viewing order history, calling the custom view 'get_orders'
    path('history/', views.get_orders, name='order_history'),

    # URL pattern for updating user details, calling the custom view 'update_user_details'
    path('update-user/', views.update_user_details, name='update_user'),
]

# In development, use Django to serve media files uploaded by users
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Use Django to serve static files like CSS, JavaScript, and images during development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
