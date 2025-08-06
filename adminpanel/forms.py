from django import forms
from shop.models import Product, Deals

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['brand', 'name', 'price', 'description', 'stock']



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class DealForm(forms.ModelForm):
    class Meta:
        model = Deals
        fields = '__all__'
