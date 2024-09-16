from django.urls import path
from .views import buscar_contenido, home

urlpatterns = [
    path('', home, name='home'), 
    path('buscar/', buscar_contenido, name='buscar_contenido'),
]