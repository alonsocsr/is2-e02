from django.urls import path
from . import views


urlpatterns = [
    path("roles/", views.crear_rol, name='crear_rol'),
    path("roles/modificar/<int:rol_id>/", views.modificar_rol, name='modificar_rol'),
    path('roles/eliminar/<int:rol_id>/', views.eliminar_rol, name='eliminar_rol'),

    path("asignarRol/", views.asignar_rol_usuario, name='asignar_rol'),
    path('modificar_usuario/<int:user_id>/', views.modificar_usuario, name='modificar_usuario'),
    path('modificar_usuario/', views.modificar_usuario, name='modificar_usuario'),

]