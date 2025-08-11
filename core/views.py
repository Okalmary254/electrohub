# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from product.models import Product, ProductImage
from django import forms
import uuid
from django.utils.text import slugify

class ProductForm(forms.ModelForm):
    image = forms.ImageField(required=False, label="Main Image")
    class Meta:
        model = Product
        fields = ['title', 'sku', 'category', 'price', 'stock', 'is_active', 'is_featured', 'description', 'make', 'weight', 'dimensions']

def home(request):
    products = Product.objects.order_by('-created_at')[:12]  # Show latest 12 products
    return render(request, 'core/home.html', {'products': products})
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})
def dashboard(request):
    # You can add stats, recent orders, etc. here
    return render(request, 'core/dashboard.html')
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            # Generate a unique slug
            base_slug = slugify(product.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
                counter += 1
            product.slug = slug
            product.save()
            image_file = form.cleaned_data.get('image')
            if image_file:
                ProductImage.objects.create(product=product, image=image_file, alt_text=product.title)
            messages.success(request, "Product added successfully.")
            return redirect('core:dashboard')
    else:
        form = ProductForm()
    return render(request, 'core/product_add.html', {'form': form})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            image_file = form.cleaned_data.get('image')
            if image_file:
                # Replace or add new image
                ProductImage.objects.update_or_create(product=product, defaults={'image': image_file, 'alt_text': product.title})
            messages.success(request, "Product updated successfully.")
            return redirect('core:dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'core/product_edit.html', {'form': form, 'product': product})