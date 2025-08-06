from django.urls import path
from . import views
from userdashboard import views as dashboard_views

urlpatterns = [
    path('', views.dashboard, name='userdashboard'),
    path('', views.dashboard_home, name='Userdashboard'),
    path('orders/', views.orders, name='user-orders'),
    path('orders/<int:order_id>/', views.order_detail, name='user-order-detail'),
    path('payments/', views.payments, name='user-payments'),
    path('profile/', views.profile, name='user-profile'),
    path('support/', views.support, name='user-support'),
    path('dashboard/', dashboard_views.dashboard, name='user_dashboard'),
]
