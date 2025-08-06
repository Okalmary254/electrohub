from multiprocessing import context
from django.shortcuts import render, get_object_or_404
from .models import Order, Payment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render


@login_required(login_url='signin')  # redirect to signin if not logged in
def dashboard(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'userdashboard/dashboard.html', {'orders': orders})


def signout(request):
    logout(request)
    return redirect('signin')  

def dashboard_home(request):
    return render(request, "userdashboard/dashboard.html", context)

@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'userdashboard/dashboard.html', {'orders': orders})

@login_required
def orders(request):
    return render(request, 'userdashboard/orders.html', {
        'orders': Order.objects.filter(user=request.user)
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'userdashboard/order_detail.html', {'order': order})

@login_required
def payments(request):
    payments = Payment.objects.filter(user=request.user)
    return render(request, 'userdashboard/payments.html', {'payments': payments})

@login_required
def profile(request):
    return render(request, 'userdashboard/profile.html')

@login_required
def support(request):
    return render(request, 'userdashboard/support.html')
