from django.urls import path, include
from django.contrib import admin
from shop import views  
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('shop.urls')),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('deals/', views.deals, name='deals'),
    path('categories/', views.categories, name='categories'),
    path('brands/', views.brands, name='brands'),
    path('support/', views.support, name='support'),
    path('userdashboard/', include('userdashboard.urls')),
    # path('userdashboard/', views.userdashboard, name='Userdashboard'), 
    path('adminpanel/', include('adminpanel.urls')),
    path('admin/', admin.site.urls),
    path('admin/', include('adminpanel.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
