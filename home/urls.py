from django.urls import path
from .views import HomeView, BuscarContenidoView

urlpatterns = [
    path('', HomeView.as_view(), name='home'), 
    path('buscar/', BuscarContenidoView.as_view(), name='buscar_contenido'),
]