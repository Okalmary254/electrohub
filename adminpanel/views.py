from django.shortcuts import render, redirect
from shop.models import Product, Order, UserProfile, Brand
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from shop.models import Product, Brand
from shop.forms import ProductForm

@staff_member_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'adminpanel/product_list.html', {'products': products})

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-products')
    else:
        form = ProductForm()
    return render(request, 'adminpanel/add_product.html', {'form': form})

@staff_member_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin-products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'adminpanel/edit_product.html', {'form': form, 'product': product})

@staff_member_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('admin-products')
    return render(request, 'adminpanel/delete_product.html', {'product': product})

def admin_dashboard(request):
    return render(request, 'adminpanel/dashboard.html')

def manage_products(request):
    products = Product.objects.all()
    return render(request, 'adminpanel/products.html', {'products': products})

def manage_orders(request):
    orders = Order.objects.all()
    return render(request, 'adminpanel/orders.html', {'orders': orders})

def manage_deals(request):
    deals = Product.objects.filter(price__lte=1000)  # Example deals logic
    return render(request, 'adminpanel/deals.html', {'deals': deals})

def manage_users(request):
    users = UserProfile.objects.all()
    return render(request, 'adminpanel/users.html', {'users': users})
