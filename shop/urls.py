from django.urls import path
from . import views

urlpatterns = [
    # ... other urls
    path('signout/', views.signout, name='signout'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
