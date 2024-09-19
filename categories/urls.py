from django.urls import path
from .views import CrearCategoriaView, ModificarCategoriaView, EliminarCategoriaView, ListarCategoriasView, DetalleCategoriaView
from django.contrib.auth.decorators import login_required, permission_required

app_name = 'categories'

urlpatterns = [
    path('gestion/',CrearCategoriaView.as_view(), name='manage'),
    path('gestion/modificar/<int:pk>/', ModificarCategoriaView.as_view(), name='modificar'),
    path('gestion/eliminar/<int:pk>/', EliminarCategoriaView.as_view(), name='eliminar'),
    path('', ListarCategoriasView.as_view(), name="listar"),
    path('<int:pk>/', DetalleCategoriaView.as_view(), name='detalle'),
]