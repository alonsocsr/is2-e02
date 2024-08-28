from django.contrib import admin
from django.urls import path, include
from categories import urls as categories_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('home.urls')),
    #path("", include('permissions.urls')),
    
    path("", include('allauth.urls')),
    path('categories/', include(categories_urls, namespace="categories")),

]
