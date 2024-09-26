from django.urls import path
from .views import UpdateProfile, categoria_interes, registrar_suscripcion, LikeView, DislikeView, EliminarCuentaView



urlpatterns = [
    path("profile/", UpdateProfile.as_view(), name='profile'),
    path("misIntereses/<int:categoria_id>/", categoria_interes, name='categoria_interes'),
    path('suscribirse/<int:categoria_id>/', registrar_suscripcion, name='registrar_suscripcion'),
    path('contenido/<int:id>/', LikeView.as_view(), name='like'),
    path('dislike/<int:id>/', DislikeView.as_view(), name='dislike'),
    path('eliminar_cuenta/', EliminarCuentaView.as_view(), name='eliminar_cuenta'),
]