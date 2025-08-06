from django.shortcuts import render
from backend.electromart.models.product import Category
from shop.models import Product, Order, UserProfile, Brand, Cart, ShippingAddress, Deals  # Add Deals

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'shop/products.html', {
        'products': products,
        'categories': categories
    })
# Home View
def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

# Deals View
def deals(request):
    deals = Deals.objects.all()
    return render(request, 'deals.html', {'deals': deals})
