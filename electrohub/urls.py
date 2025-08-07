# electrohub/urls.py — this is your MAIN PROJECT urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("products/", include('product.urls')),
    path("cart/", include('cart.urls', namespace='cart')),
    path("orders/", include('order.urls', namespace='order')),
    path("auth/", include('authapp.urls', namespace='authapp')),
    # path("", include('users.urls', namespace='users')),  
    path("", include('core.urls', namespace='core')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
