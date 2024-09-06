from django import views
from django.urls import path
from .views import CambiarEstadoView, ContenidoBorradorList, CrearContenido
from . import views
app_name = 'content'

urlpatterns = [
    path("crear-contenido/", CrearContenido.as_view(), name='crear_contenido'),
    path("editar_contenido/<int:id>/", views.editar_contenido, name='editar_contenido'),
    path('vista_editor/', views.vista_Editor, name='vista_editor'),
    path('vista_publicador/', views.vista_Publicador, name='vista_publicador'),
    path("inactivar_contenido/<int:id>/", views.inactivar_contenido, name='inactivar_contenido'),
    path("mis-borradores/", ContenidoBorradorList.as_view(), name='lista_borradores'),
    path("editar/<int:contenido_id>/", CrearContenido.as_view(), name='crear_contenido'),
    path('cambiar-estado/<int:pk>/', CambiarEstadoView.as_view(), name='cambiar_estado'),
]