from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Cart pages
    path('', views.cart_detail, name='detail'),
    
    # Cart actions
    path('add/', views.add_to_cart, name='add'),
    path('update/', views.update_cart_item, name='update'),
    path('remove/', views.remove_from_cart, name='remove'),
    path('clear/', views.clear_cart, name='clear'),
    
    # Ajax endpoints
    path('ajax/summary/', views.cart_summary, name='summary'),
    path('ajax/mini-cart/', views.mini_cart, name='mini_cart'),
]