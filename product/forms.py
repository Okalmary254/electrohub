from django import forms
from django.contrib.auth.models import User
from .models import Product, Category, ProductReview


class ProductSearchForm(forms.Form):
    """Form for searching products"""
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search products...',
            'class': 'form-control'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Min Price',
            'class': 'form-control',
            'step': '0.01'
        })
    )
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Max Price',
            'class': 'form-control',
            'step': '0.01'
        })
    )
    make = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Brand/Make',
            'class': 'form-control'
        })
    )


class ProductReviewForm(forms.ModelForm):
    """Form for submitting product reviews"""
    
    class Meta:
        model = ProductReview
        fields = ['rating', 'title', 'review_text']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-control'}
            ),
            'title': forms.TextInput(attrs={
                'placeholder': 'Review title',
                'class': 'form-control'
            }),
            'review_text': forms.Textarea(attrs={
                'placeholder': 'Write your review here...',
                'class': 'form-control',
                'rows': 4
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})


class ProductFilterForm(forms.Form):
    """Form for filtering products on category pages"""
    SORT_CHOICES = [
        ('', 'Default'),
        ('price_low', 'Price: Low to High'),
        ('price_high', 'Price: High to Low'),
        ('name_az', 'Name: A to Z'),
        ('name_za', 'Name: Z to A'),
        ('newest', 'Newest First'),
        ('rating', 'Highest Rated'),
    ]
    
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    in_stock_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    featured_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )