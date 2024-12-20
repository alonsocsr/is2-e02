from django.contrib import admin
from django.urls import path, include
from categories import urls as categories_urls

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", include('home.urls')),
    path("", include('profiles.urls')),
    path('', include('permissions.urls')),
    path('', include('content.urls')),
    
    path("", include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('categorias/', include(categories_urls, namespace="categories")),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)