from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import CartItem


class AddToCartForm(forms.Form):
    """Form for adding products to cart"""
    quantity = forms.IntegerField(
        initial=1,
        min_value=1,
        max_value=99,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '99',
            'style': 'width: 80px;'
        })
    )


class UpdateCartItemForm(forms.ModelForm):
    """Form for updating cart item quantities"""
    
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control cart-quantity-input',
                'min': '1',
                'max': '99',
                'style': 'width: 80px;'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].validators = [MinValueValidator(1), MaxValueValidator(99)]


class CartCouponForm(forms.Form):
    """Form for applying discount coupons"""
    coupon_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter coupon code',
        })
    )
