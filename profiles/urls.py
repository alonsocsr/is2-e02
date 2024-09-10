from django.urls import path
from .views import UpdateProfile, categoria_interes, registrar_suscripcion



urlpatterns = [
    path("profile/", UpdateProfile.as_view(), name='profile'),
    path("misIntereses/<int:categoria_id>/", categoria_interes, name='categoria_interes'),
    path('suscribirse/<int:categoria_id>/', registrar_suscripcion, name='registrar_suscripcion'),
]