from django.contrib import admin
from .models import Product, Category, Order, OrderItem, UserProfile, Brand, Cart, ShippingAddress

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(UserProfile)
admin.site.register(Brand)
admin.site.register(Cart)
admin.site.register(ShippingAddress)
