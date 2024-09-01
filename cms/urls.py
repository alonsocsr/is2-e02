from django.contrib import admin
from django.urls import path, include
from categories import urls as categories_urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('home.urls')),
    path("", include('profiles.urls')),
    path('', include('permissions.urls')),
    
    path("", include('allauth.urls')),
    path('categories/', include(categories_urls, namespace="categories")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
