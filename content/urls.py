from django import views
from django.urls import path
from .views import CambiarEstadoView, ContenidoBorradorList, CrearContenido
from . import views

urlpatterns = [
    #borrador
    path("mis-borradores/", ContenidoBorradorList.as_view(), name='lista_borradores'),
    path("crear-contenido/", CrearContenido.as_view(), name='crear_contenido_nuevo'),
    path("editar/<int:contenido_id>/", CrearContenido.as_view(), name='crear_contenido'),
    path('cambiar-estado/<int:pk>/', CambiarEstadoView.as_view(), name='cambiar_estado'),
    #edicion
    path("editar_contenido/<int:id>/", views.editar_contenido, name='editar_contenido'),
    path('vista_editor/', views.vista_Editor, name='vista_editor'),
    #publicador
    path('vista_publicador/', views.vista_Publicador, name='vista_publicador'),
    path("inactivar_contenido/<int:id>/", views.inactivar_contenido, name='inactivar_contenido'),
    
]