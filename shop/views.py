from re import search

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .serializer import CategorySerializer, ProductSerializer, CartSerializer, OrderSerializer
from .models import Category, Product, Cart, CartItem, Order, OrderItem
# Create your views here.

class CategoryViewset(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

# --------------------product viewset with search and filter functionality
class ProductViewset(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):

        queryset = Product.objects.all()

        search = self.request.query_params.get("search")

        category = self.request.query_params.get("category")

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        if category:
            queryset = queryset.filter(
                category_id=category
            )

        return queryset


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        product_id = request.data.get("product_id")

        quantity = int(
            request.data.get("quantity", 1)
        )

        product = get_object_or_404(
            Product,
            id=product_id
        )

        if quantity <= 0:
            return Response(
                {"error": "Quantity must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if product.stock < quantity:
            return Response(
                {"error": "Not enough stock available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:

            # Check total quantity after update
            new_quantity = cart_item.quantity + quantity

            if new_quantity > product.stock:
                return Response(
                    {"error": "Not enough stock available"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item.quantity = new_quantity
            cart_item.save()

        return Response(
            {"message": "Product added to cart"},
            status=status.HTTP_201_CREATED
        )

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        cart, created = Cart.objects.get_or_create(user=request.user) # get the cart for the current user 

        serializer = CartSerializer(cart) #items = cart.items.all() , we are accessing all cart item with the help of nested serializers

        return Response(serializer.data)
    

#update the quantity of cartitem
class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, item_id):

        quantity = request.data.get("quantity") #quantity that user sent
        if quantity <= 0:
            return Response(
                {"error":"Invalid quantity"},
                 status=400
                )

        cart_item =get_object_or_404(CartItem,
            id=item_id,
            cart__user=request.user
        )

        cart_item.quantity = quantity
        cart_item.save()

        return Response({
            "message": "Cart updated"
        })
    
class RemoveCartItemView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, item_id):

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )

        cart_item.delete()

        return Response({
            "message": "Item removed from cart"
        })
    



class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):

        cart = get_object_or_404(
            Cart,
            user=request.user
        )

        order = Order.objects.create(
            user=request.user
        )

        total_price = 0

        for item in cart.items.all():

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.price
                
            )
            item.product.stock -= item.quantity
            item.product.save()

            total_price += (
                item.product.price *
                item.quantity
            )

        order.total_price = total_price
        order.save()

        cart.items.all().delete()

        return Response({
            "message": "Order placed successfully"
        })
    


class OrderListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.user
        )
    
class OrderDetailView(RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.user
        )