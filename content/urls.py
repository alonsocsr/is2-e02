from django.urls import path
from .views import CambiarEstadoView, ContenidoBorradorList, CrearContenido, ContenidoEdicionList, EditarContenido, ContenidoPublicarList, RechazarContenido, VistaAllContenidos, VistaContenido
from . import views
urlpatterns = [
    #autor
    path("mis-borradores/", ContenidoBorradorList.as_view(), name='lista_borradores'),
    path("crear-contenido/", CrearContenido.as_view(), name='crear_contenido_nuevo'),
    path("editar/<int:contenido_id>/", CrearContenido.as_view(), name='crear_contenido'),

    #editor
    path('vista-editor/', ContenidoEdicionList.as_view(), name='vista_editor'),
    path("editar-contenido/<int:contenido_id>/", EditarContenido.as_view(), name='editar_contenido'),

    #publicador
    path('publicar/', ContenidoPublicarList.as_view(), name='vista_publicador'),
    
    #cambiar estado
    path('cambiar-estado/<int:pk>/', CambiarEstadoView.as_view(), name='cambiar_estado'),
    
    #vista de contenidos
    path('contenidos/', VistaAllContenidos.as_view(), name='vista_all_contenidos'),
    path('detalle-contenido/<slug:slug>/', VistaContenido.as_view(), name='detalle_contenido'),
    
    path('rechazar-contenido/<int:pk>', RechazarContenido.as_view(), name='rechazar_contenido'),
]