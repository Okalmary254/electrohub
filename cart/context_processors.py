from .models import Cart


def cart_context(request):
    """Context processor to add cart information to all templates"""
    cart_total_items = 0
    cart_total_price = 0
    
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            if request.session.session_key:
                cart = Cart.objects.filter(session_key=request.session.session_key).first()
            else:
                cart = None
        
        if cart:
            cart_total_items = cart.total_items
            cart_total_price = cart.total_price
    except:
        # Handle any database errors gracefully
        pass
    
    return {
        'cart_total_items': cart_total_items,
        'cart_total_price': cart_total_price,
    }
