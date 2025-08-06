from django.contrib import admin
from .models import Product, Order, UserProfile, Brand, Cart, ShippingAddress

admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Order)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(ShippingAddress)
