from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Cart, CartItem, Review
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','description','price','category']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at', 'is_paid']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','quantity', 'price']
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at','updated_at']
    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'created_at', 'updated_at']
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user','product', 'rating', 'created']