from django.urls import path
from .views import CrearCategoriaView, ModificarCategoriaView, EliminarCategoriaView
from django.contrib.auth.decorators import login_required, permission_required

app_name = 'categories'

urlpatterns = [
    path('gestion/', login_required(permission_required('permissions.crear_categoria')(CrearCategoriaView.as_view())), name='manage'),
    path('gestion/modificar/<int:pk>/', login_required(permission_required('permissions.modificar_categoria')(ModificarCategoriaView.as_view())), name='modificar'),
    path('gestion/eliminar/<int:pk>/', login_required(permission_required('permissions.eliminar_categoria')(EliminarCategoriaView.as_view())), name='eliminar'),
]