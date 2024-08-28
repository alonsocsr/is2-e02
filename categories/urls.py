from django.urls import path
from .views import CrearCategoriaView, CategoriaListView

app_name = 'categories'

urlpatterns = [
    path('manage/', CrearCategoriaView.as_view(), name='manage'),
]
