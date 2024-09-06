from django.urls import path
from .views import CrearContenido, ContenidoBorradorList, CambiarEstadoView


urlpatterns = [
    path("mis-borradores/", ContenidoBorradorList.as_view(), name='lista_borradores'),
    path("editar/<int:contenido_id>/", CrearContenido.as_view(), name='crear_contenido'),
    path("crear-contenido/", CrearContenido.as_view(), name='crear_contenido_nuevo'),
    path('cambiar-estado/<int:pk>/', CambiarEstadoView.as_view(), name='cambiar_estado'),
]