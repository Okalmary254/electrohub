from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.db import transaction
import json

from .models import Cart, CartItem
from .forms import AddToCartForm, UpdateCartItemForm, CartCouponForm
from product.models import Product


def get_or_create_cart(request):
    """Get or create cart for current user/session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def cart_detail(request):
    """Display cart contents"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'coupon_form': CartCouponForm(),
    }
    return render(request, 'cart/cart_detail.html', context)


@require_POST
def add_to_cart(request):
    """Add product to cart - supports both Ajax and regular requests"""
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    form = AddToCartForm(request.POST)
    
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        
        # Check stock availability
        if quantity > product.stock:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': f'Only {product.stock} items available in stock.'
                })
            messages.error(request, f'Only {product.stock} items available in stock.')
            return redirect('product:detail', slug=product.slug)
        
        cart = get_or_create_cart(request)
        
        with transaction.atomic():
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                # Update existing item
                new_quantity = cart_item.quantity + quantity
                if new_quantity > product.stock:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': False,
                            'error': f'Cannot add {quantity} items. Only {product.stock - cart_item.quantity} more available.'
                        })
                    messages.error(request, f'Cannot add {quantity} items. Only {product.stock - cart_item.quantity} more available.')
                    return redirect('product:detail', slug=product.slug)
                
                cart_item.quantity = new_quantity
                cart_item.save()
        
        # Ajax response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'{product.title} added to cart successfully!',
                'cart_total_items': cart.total_items,
                'cart_total_price': str(cart.total_price),
                'item_subtotal': str(cart_item.subtotal)
            })
        
        # Regular response
        messages.success(request, f'{product.title} added to cart successfully!')
        return redirect('cart:detail')
    
    # Form validation errors
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'error': 'Invalid quantity specified.'
        })
    
    messages.error(request, 'Invalid quantity specified.')
    return redirect('product:detail', slug=product.slug)


@require_POST
def update_cart_item(request):
    """Update cart item quantity - Ajax only"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Ajax request required'})
    
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({'success': False, 'error': 'Invalid data'})
    
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    # Validate quantity
    if quantity < 1:
        return JsonResponse({'success': False, 'error': 'Quantity must be at least 1'})
    
    if quantity > cart_item.product.stock:
        return JsonResponse({
            'success': False,
            'error': f'Only {cart_item.product.stock} items available in stock.'
        })
    
    # Update quantity
    cart_item.quantity = quantity
    cart_item.save()
    
    return JsonResponse({
        'success': True,
        'item_subtotal': str(cart_item.subtotal),
        'cart_total_items': cart.total_items,
        'cart_total_price': str(cart.total_price)
    })


@require_POST
def remove_from_cart(request):
    """Remove item from cart - supports both Ajax and regular requests"""
    item_id = request.POST.get('item_id')
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    product_title = cart_item.product.title
    cart_item.delete()
    
    # Ajax response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product_title} removed from cart.',
            'cart_total_items': cart.total_items,
            'cart_total_price': str(cart.total_price)
        })
    
    # Regular response
    messages.success(request, f'{product_title} removed from cart.')
    return redirect('cart:detail')


@require_POST
def clear_cart(request):
    """Clear all items from cart"""
    cart = get_or_create_cart(request)
    item_count = cart.items.count()
    cart.items.all().delete()
    
    # Ajax response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'Cart cleared. {item_count} items removed.',
            'cart_total_items': 0,
            'cart_total_price': '0.00'
        })
    
    # Regular response
    messages.success(request, f'Cart cleared. {item_count} items removed.')
    return redirect('cart:detail')


def cart_summary(request):
    """Get cart summary - Ajax only"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Ajax request required'})
    
    cart = get_or_create_cart(request)
    
    return JsonResponse({
        'success': True,
        'total_items': cart.total_items,
        'total_price': str(cart.total_price),
        'items': [
            {
                'id': item.id,
                'product_title': item.product.title,
                'product_slug': item.product.slug,
                'quantity': item.quantity,
                'price': str(item.product.price),
                'subtotal': str(item.subtotal)
            }
            for item in cart.items.select_related('product').all()
        ]
    })


def mini_cart(request):
    """Render mini cart widget - Ajax only"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Ajax request required'})
    
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()[:5]  # Show only first 5 items
    
    html = render_to_string('cart/mini_cart.html', {
        'cart': cart,
        'cart_items': cart_items,
    }, request=request)
    
    return JsonResponse({
        'success': True,
        'html': html,
        'total_items': cart.total_items,
        'total_price': str(cart.total_price)
    })
