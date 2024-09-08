from django.urls import path
from .views import CambiarEstadoView, ContenidoBorradorList, CrearContenido, ContenidoEdicionList, EditarContenido, ContenidoPublicarList, RechazarContenido

urlpatterns = [
    path("mis-borradores/", ContenidoBorradorList.as_view(), name='lista_borradores'),
    path("crear-contenido/", CrearContenido.as_view(), name='crear_contenido_nuevo'),
    path("editar/<int:contenido_id>/", CrearContenido.as_view(), name='crear_contenido'),

    path('vista-editor/', ContenidoEdicionList.as_view(), name='vista_editor'),
    path("editar-contenido/<int:contenido_id>/", EditarContenido.as_view(), name='editar_contenido'),

    path('vista_publicador/', ContenidoPublicarList.as_view(), name='vista_publicador'),

    path('cambiar-estado/<int:pk>/', CambiarEstadoView.as_view(), name='cambiar_estado'),
    path('rechazar-contenido/<int:pk>', RechazarContenido.as_view(), name='rechazar_contenido'),
]