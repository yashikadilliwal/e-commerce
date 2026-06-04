from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewset,
    ProductViewset,
    AddToCartView,
    CartView,
    UpdateCartItemView,
    RemoveCartItemView,
    CheckoutView,
    OrderListView,
    OrderDetailView,
)

router = DefaultRouter()
router.register('categories', CategoryViewset, basename='category')
router.register('products', ProductViewset, basename='product')

urlpatterns = [
    # Category & Product CRUD
    path('', include(router.urls)),

    # Cart
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/item/<int:item_id>/update/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('cart/item/<int:item_id>/remove/', RemoveCartItemView.as_view(), name='remove-cart-item'),

    # Checkout
    path('checkout/', CheckoutView.as_view(), name='checkout'),

    # Orders
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]