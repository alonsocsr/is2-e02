from django.urls import path
from .views import CrearContenido


urlpatterns = [
    path("crear_contenido/", CrearContenido.as_view(), name='crear_contenido'),
]