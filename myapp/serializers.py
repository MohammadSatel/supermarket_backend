from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Category, Product, Order, OrderDetail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User


# serializers for models
class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
  
class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderDetailSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
    quantity = serializers.IntegerField(required=True)  # You can adjust the default value as needed

    class Meta:
        model = OrderDetail
        fields = ['quantity', 'product']

class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['user', 'orderDate', 'total_price', 'order_details']

    def create(self, validated_data):
        order_details_data = validated_data.pop('order_details', [])
        order = Order.objects.create(**validated_data)

        for order_detail_data in order_details_data:
            OrderDetail.objects.create(order=order, **order_detail_data)

        return order
          
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # Custom logic for creating a user, if needed
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Custom logic for updating a user, if needed
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        
        # Handle password separately to ensure proper hashing
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance
