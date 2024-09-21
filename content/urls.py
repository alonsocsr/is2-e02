from django.urls import path
from .views import CambiarEstadoView, ContenidoBorradorList, ContenidoInactivadoList, CrearContenido, ContenidoEdicionList, EditarContenido, ContenidoPublicarList, RechazarContenido, VistaAllContenidos, VistaContenido, InactivarContenido, VistaContenidosReportados, TableroKanbanView,  UpdatePostStatusView, ContentStatusHistoryView, CalificarContenidoView, SeleccionarContenido
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
    path('inactivar-contenido/<int:pk>', InactivarContenido.as_view(), name='inactivar_contenido'),
    
    #vista de contenidos
    path('contenidos/', VistaAllContenidos.as_view(), name='vista_all_contenidos'),
    path('detalle-contenido/<slug:slug>/', VistaContenido.as_view(), name='detalle_contenido'),
    
    path('rechazar-contenido/<int:pk>', RechazarContenido.as_view(), name='rechazar_contenido'),
    path('contenidos-reportados', VistaContenidosReportados.as_view(), name='contenidos_reportados'),
    path('contenidos-inactivos', ContenidoInactivadoList.as_view(), name='contenidos_inactivados'),
    path('contenido/<slug:slug>/select/', SeleccionarContenido.as_view(), name='contenido_seleccionado'),

    #tablero kanban
    path('tablero-kanban/', TableroKanbanView.as_view(), name='tablero_kanban'),
    path('update-post-status/',  UpdatePostStatusView.as_view(), name='update_post_status'),
    # urls.py

    #historial
    path('historial-cambios/', ContentStatusHistoryView.as_view(), name='content_status_history'),

    #calificacion
    path('contenido/<int:contenido_id>/calificar/', CalificarContenidoView.as_view(), name='calificar_contenido'),
]