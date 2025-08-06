from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from shop.models import Product, Order, UserProfile, Brand, Cart, ShippingAddress
from .forms import SignupForm, SigninForm
from django.contrib.auth import logout

def signout(request):
    logout(request)
    return redirect('signin') 


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('userdashboard')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'shop/signin.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, f'Account created for {user.username}')
            return redirect('home')  
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()

    # return render(request, 'signup.html', {'form': form})
        user = user.objects.create_user(...)  # or whatever you're doing
        login(request, user)
        return redirect('user_dashboard')  # redirect after successful signup
    return render(request, 'shop/signup.html')        

def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def deals(request):
    return render(request, 'deals.html')


def categories(request):
    return render(request, 'categories.html')


def brands(request):
    return render(request, 'brands.html')


def support(request):
    return render(request, 'support.html')


def Userdashboard(request):
    return render(request, 'Userdashboard.html')
