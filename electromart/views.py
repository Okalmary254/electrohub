from django.shortcuts import render
from shop.models import Product
from shop.models import Product, Order, UserProfile, Brand, Cart, ShippingAddress

def home(request):
    products = Product.objects.all()
    return render(request, 'templates/index.html', {'products': products})
