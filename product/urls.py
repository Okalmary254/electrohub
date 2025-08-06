from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    # Product URLs
    path('', views.product_list, name='list'),
    path('search/', views.search, name='search'),
    path('featured/', views.featured_products, name='featured'),
    path('ajax/quick-search/', views.quick_search, name='quick_search'),
    
    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    
    # Brand URLs
    path('brands/', views.brands, name='brands'),
    path('brand/<str:make>/', views.brand_products, name='brand_products'),
    
    # Product detail and review URLs
    path('<slug:slug>/', views.product_detail, name='detail'),
    path('<slug:slug>/review/', views.add_review, name='add_review'),
]