from rest_framework import serializers
from .models import Category, Product, Order, OrderItem, Cart, CartItem, Review
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'verbose_name': "Название"}
        }

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category')

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'category_id']
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'verbose_name': "Название"},
            'description': {'verbose_name': "Описание"},
            'price': {'verbose_name': "Цена"},
            'category': {'verbose_name': "Категория"},
            'category_id': {'verbose_name': "Категория ID"}
        }

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product')

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_id', 'quantity', 'price']
        extra_kwargs = {
            'id': {'read_only': True},
            'order': {'verbose_name': "Заказ"},
            'product': {'verbose_name': "Продукт"},
            'product_id': {'verbose_name': "Продукт ID"},
            'quantity': {'verbose_name': "Количество"},
            'price': {'verbose_name': "Цена"}
        }

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'is_paid', 'items']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'verbose_name': "Пользователь"},
            'created_at': {'verbose_name': "Создан"},
            'updated_at': {'verbose_name': "Обновлен"},
            'is_paid': {'verbose_name': "Оплачен"},
            'items': {'verbose_name': "Элементы заказа"}
        }

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product')

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'product_id', 'quantity', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'cart': {'verbose_name': "Корзина"},
            'product': {'verbose_name': "Продукт"},
            'product_id': {'verbose_name': "Продукт ID"},
            'quantity': {'verbose_name': "Количество"},
            'created_at': {'read_only': True, 'verbose_name': "Создан"},
            'updated_at': {'read_only': True, 'verbose_name': "Обновлен"}
        }

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'items']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'verbose_name': "Пользователь"},
            'created_at': {'verbose_name': "Создан"},
            'updated_at': {'verbose_name': "Обновлен"},
            'items': {'verbose_name': "Элементы корзины"}
        }
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        field =  ['id', 'user', 'product', 'rating', 'comment', 'created_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'product': {'read_only': True},
            'created_at': {'read_only': True},
        }
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True, write_only=True)