from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, OrderViewSet, CartViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartViewSet.as_view({'get': 'list'}), name='cart-detail'),
    path('cart/add/', CartViewSet.as_view({'post': 'add_item'}), name='cart-add-item'),
    path('cart/remove/<int:pk>/', CartViewSet.as_view({'delete': 'remove_item'}), name='cart-remove-item'),
]
