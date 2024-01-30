from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product, Order, OrderDetail
from .serializers import CategorySerializer, MyTokenObtainPairSerializer, OrderSerializer, ProductSerializer, UserSerializer, OrderDetailSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes


# Login - get token with payload from sirializer
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST', 'PUT'])
def register_or_update_user(req):
    if req.method == 'POST':
        serializer = UserSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif req.method == 'PUT':
        username = req.data.get("username")
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Register - get username & pass and create new user
@api_view(['POST'])
def register(req):
    User.objects.create_user(username=req.data["username"], password=req.data["password"], email=req.data["email"])
    return Response({"user":"created successfuly"})
 
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
        "email@gmail.com",
        [user.email],
        fail_silently=False,
    )

# get cart from user and save it to Order and OrderDetail
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

    return Response("order saved fucking successfuly", status=status.HTTP_201_CREATED)

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

    user_data = {
        "username": user.username,
        "email": user.email,
    }
    
    response_data = {
        "user": user_data,
        "orders": orders_data
    }

    return Response(response_data)

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

# Full CRUD using serializer for product & categoy models. 
# not really needed for now because i'm using "/admin"
class ProductsView(APIView):
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