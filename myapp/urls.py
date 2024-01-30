from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


# URL patterns
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('products/', views.ProductsView.as_view(), name='product_list'),
    path('categories/', views.CategoriesView.as_view(), name='category_list'),
    path('checkout/', views.checkOut, name='checkout'),
    path('products/<int:catID>/', views.ProductsView.as_view(), name='product_by_category'),
    path('history/', views.get_orders, name='order_history'),
    path('update-user/', views.update_user_details, name='update_user'),
]

# In development, use Django to serve media files uploaded by users
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Use Django to serve static files like CSS, JavaScript, and images during development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
