from django.urls import path
from .views import UpdateProfile, VerHistorialCompras, categoria_interes, registrar_suscripcion, LikeView, DislikeView, EliminarCuentaView
from . import views


urlpatterns = [
    path("profile/", UpdateProfile.as_view(), name='profile'),
    path("misIntereses/<int:categoria_id>/", categoria_interes, name='categoria_interes'),
    path('suscribirse/<int:categoria_id>/', registrar_suscripcion, name='registrar_suscripcion'),
    path('contenido/<int:id>/', LikeView.as_view(), name='like'),
    path('dislike/<int:id>/', DislikeView.as_view(), name='dislike'),
    path('eliminar_cuenta/', EliminarCuentaView.as_view(), name='eliminar_cuenta'),
    path('historial-compras/', VerHistorialCompras.as_view(), name='ver_historial_compras'),
     path('exportar/compras/xlsx/', views.exportar_compras_xlsx, name='exportar_compras_xlsx'),
]