# core/views.py

from django.shortcuts import render

def home(request):
    return render(request, 'base.html')
def product_list(request):
    from product.models import Product
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})
def dashboard(request):
    # You can add stats, recent orders, etc. here
    return render(request, 'core/dashboard.html')
def product_add(request):
    # Implement your product add logic here
    pass