from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),

    # Product Management
    path('products/', views.product_list, name='products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # Orders, Deals, Users (placeholders — define their views later)
    path('orders/', views.manage_orders, name='admin-orders'),
    path('deals/', views.manage_deals, name='admin-deals'),
    path('users/', views.manage_users, name='admin-users'),
]
