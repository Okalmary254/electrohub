from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful.")
            return redirect('core:home')  # Redirect to landing page
    else:
        form = UserCreationForm()
    return render(request, 'authapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('authapp:profile')
            else:
                messages.error(request, "User not found.")
        else:
            messages.error(request, "User not found.")
    else:
        form = AuthenticationForm()
    return render(request, 'authapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('authapp:login')

@login_required
def profile_view(request):
    return render(request, 'authapp/profile.html', {'user': request.user})
