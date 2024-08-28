from django.urls import path
from .views import CrearCategoriaView, CategoriaListView

app_name = 'categories'

urlpatterns = [
    path('new/', CrearCategoriaView.as_view(), name='crear_categoria'),
]
