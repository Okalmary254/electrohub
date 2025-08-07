from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("products/", include('product.urls')),
    path("cart/", include('cart.urls')),
    path("orders/", include('order.urls')),
    path("auth/", include('auth.urls')),  # Ensure this matches your auth app's urls.py
    path("", include('electrohub.urls')),  # Main app URLs
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
