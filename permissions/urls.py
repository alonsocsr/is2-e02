from django.urls import path
from . import views

urlpatterns = [
    path("crearRol/", views.crear_rol, name='crear_rol'),
    path("asignarRol/", views.asignar_rol_usuario, name='asignar_rol'),
]