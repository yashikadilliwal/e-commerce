from django.shortcuts import render
from .models import Product

def home(request):

    products = Product.objects.all()[:8]

    return render(
        request,
        "home.html",
        {"products": products}
    )