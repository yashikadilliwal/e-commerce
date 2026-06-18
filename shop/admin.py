from django.contrib import admin

# Register your models here.

from .models import Category, Product, Cart, CartItem, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created_at",
        "updated_at"
    )

    search_fields = (
        "name",
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "category",
        "price",
        "stock",
        "created_at"
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
        "description"
    )

    prepopulated_fields = {}

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "created_at"
    )

    search_fields = (
        "user__username",
    )

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "cart",
        "product",
        "quantity"
    )

    search_fields = (
        "product__name",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "total_price",
        "created_at"
    )

    search_fields = (
        "user__username",
    )

    ordering = (
        "-created_at",
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "status"
    )

    list_filter = (
        "status",
    )

admin.site.site_header = "E-Commerce Administration"

admin.site.site_title = "E-Commerce Admin"

admin.site.index_title = "Welcome to Dashboard"
