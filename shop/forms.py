from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from shop.models import Product, Deals


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

class SigninForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class DealForm(forms.ModelForm):
    class Meta:
        model = Deals
        fields = '__all__'
