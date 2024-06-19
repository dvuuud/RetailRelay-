from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category, Product, Order, OrderItem, Cart, CartItem, Review
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, CartSerializer, CartItemSerializer, UserSerializer, ReviewSerializer

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class CartItemListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        return cart.items.all()

    def perform_create(self, serializer):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        serializer.save(cart=cart)

class CartItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        return cart.items.all()

class UserInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_info = {
            'username': request.user.username,
            'email': request.user.email,
        }
        return Response(user_info)

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer