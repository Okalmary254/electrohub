from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django.db.models import Case, When, Value, IntegerField

from .models import Product, Category, ProductReview, ProductImage
from .forms import ProductSearchForm, ProductReviewForm, ProductFilterForm


def product_list(request):
    """List all products with search and filtering"""
    products = Product.objects.filter(is_active=True).select_related('category')
    form = ProductSearchForm(request.GET)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        make = form.cleaned_data.get('make')
        
        if query:
            products = products.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(make__icontains=query)
            )
        
        if category:
            products = products.filter(category=category)
        
        if min_price:
            products = products.filter(price__gte=min_price)
        
        if max_price:
            products = products.filter(price__lte=max_price)
        
        if make:
            products = products.filter(make__icontains=make)
    
    # Add sorting
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name_az':
        products = products.order_by('title')
    elif sort_by == 'name_za':
        products = products.order_by('-title')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'rating':
        products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'total_products': paginator.count,
    }
    
    return render(request, 'product/product_list.html', context)


def product_detail(request, slug):
    """Product detail view with reviews"""
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related(
            'images', 'reviews__user'
        ),
        slug=slug,
        is_active=True
    )
    
    # Get product reviews
    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
    
    # Calculate average rating
    avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
    total_reviews = reviews.count()
    
    # Rating distribution
    rating_distribution = {}
    for i in range(1, 6):
        rating_distribution[i] = reviews.filter(rating=i).count()
    
    # Check if user has already reviewed this product
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    
    # Related products (same category, excluding current product)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    # Review form
    review_form = ProductReviewForm()
    
    context = {
        'product': product,
        'reviews': reviews[:10],  # Show first 10 reviews
        'avg_rating': avg_rating,
        'total_reviews': total_reviews,
        'rating_distribution': rating_distribution,
        'user_review': user_review,
        'related_products': related_products,
        'review_form': review_form,
    }
    
    return render(request, 'product/product_detail.html', context)


def category_list(request):
    """List all categories"""
    categories = Category.objects.filter(
        is_active=True, 
        parent=None
    ).prefetch_related('subcategories')
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'product/category_list.html', context)


def category_detail(request, slug):
    """Category detail view with products"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    # Get all products in this category and subcategories
    subcategory_ids = list(category.subcategories.values_list('id', flat=True))
    category_ids = [category.id] + subcategory_ids
    
    products = Product.objects.filter(
        category_id__in=category_ids,
        is_active=True
    ).select_related('category')
    
    # Apply filters
    filter_form = ProductFilterForm(request.GET)
    if filter_form.is_valid():
        sort_by = filter_form.cleaned_data.get('sort_by')
        in_stock_only = filter_form.cleaned_data.get('in_stock_only')
        featured_only = filter_form.cleaned_data.get('featured_only')
        
        if in_stock_only:
            products = products.filter(stock__gt=0)
        
        if featured_only:
            products = products.filter(is_featured=True)
        
        # Apply sorting
        if sort_by == 'price_low':
            products = products.order_by('price')
        elif sort_by == 'price_high':
            products = products.order_by('-price')
        elif sort_by == 'name_az':
            products = products.order_by('title')
        elif sort_by == 'name_za':
            products = products.order_by('-title')
        elif sort_by == 'newest':
            products = products.order_by('-created_at')
        elif sort_by == 'rating':
            products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'filter_form': filter_form,
        'total_products': paginator.count,
    }
    
    return render(request, 'product/category_detail.html', context)


@login_required
@require_POST
def add_review(request, slug):
    """Add a product review"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Check if user has already reviewed this product
    existing_review = ProductReview.objects.filter(
        product=product,
        user=request.user
    ).first()
    
    if existing_review:
        messages.error(request, 'You have already reviewed this product.')
        return redirect('product:detail', slug=slug)
    
    form = ProductReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()
        
        messages.success(request, 'Your review has been submitted successfully!')
        return redirect('product:detail', slug=slug)
    else:
        messages.error(request, 'Please correct the errors in your review.')
        return redirect('product:detail', slug=slug)


def search(request):
    """Advanced product search"""
    form = ProductSearchForm(request.GET)
    products = Product.objects.none()
    
    if form.is_valid() and any(form.cleaned_data.values()):
        products = Product.objects.filter(is_active=True).select_related('category')
        
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        make = form.cleaned_data.get('make')
        
        if query:
            products = products.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(make__icontains=query) |
                Q(sku__icontains=query)
            )
        
        if category:
            # Include subcategories
            subcategory_ids = list(category.subcategories.values_list('id', flat=True))
            category_ids = [category.id] + subcategory_ids
            products = products.filter(category_id__in=category_ids)
        
        if min_price:
            products = products.filter(price__gte=min_price)
        
        if max_price:
            products = products.filter(price__lte=max_price)
        
        if make:
            products = products.filter(make__icontains=make)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'total_products': paginator.count,
        'search_performed': any(form.cleaned_data.values()) if form.is_valid() else False,
    }
    
    return render(request, 'product/search.html', context)


def featured_products(request):
    """List featured products"""
    products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('category').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_products': paginator.count,
    }
    
    return render(request, 'product/featured_products.html', context)


def brands(request):
    """List all brands/makes"""
    brands = Product.objects.filter(
        is_active=True
    ).values_list('make', flat=True).distinct().order_by('make')
    
    context = {
        'brands': brands,
    }
    
    return render(request, 'product/brands.html', context)


def brand_products(request, make):
    """List products by brand/make"""
    products = Product.objects.filter(
        make__iexact=make,
        is_active=True
    ).select_related('category')
    
    if not products.exists():
        messages.error(request, f'No products found for brand "{make}".')
        return redirect('product:brands')
    
    # Apply sorting
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name_az':
        products = products.order_by('title')
    elif sort_by == 'name_za':
        products = products.order_by('-title')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'make': make,
        'page_obj': page_obj,
        'total_products': paginator.count,
    }
    
    return render(request, 'product/brand_products.html', context)


# AJAX Views
def quick_search(request):
    """AJAX endpoint for quick search suggestions"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    products = Product.objects.filter(
        Q(title__icontains=query) | Q(make__icontains=query),
        is_active=True
    )[:10]
    
    results = []
    for product in products:
        results.append({
            'title': product.title,
            'make': product.make,
            'price': str(product.price),
            'url': f'/products/{product.slug}/',
        })
    
    return JsonResponse({'results': results})
