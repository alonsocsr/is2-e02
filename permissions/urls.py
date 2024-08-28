from django.urls import path
from . import views

urlpatterns = [
    path("crearRol/", views.crear_rol, name='crear_rol'),
]