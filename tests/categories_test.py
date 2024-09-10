import pytest
from django.urls import reverse
from categories.models import Categorias
from django.contrib.messages import get_messages
from django.shortcuts import redirect


@pytest.mark.django_db
def test_crear_categoria(client, setup):
    """
    Test para verificar que se puede crear una categoría.
    """
    user, _ = setup

    data = {
        'nombre_categoria': 'Categoría de prueba',
        'descripcion': 'Descripción de prueba',
        'descripcion_corta': 'Corta',
        'tipo_categoria': 'PU'
    }
    
    print(f"\n\nProbando la creación de la categoría de prueba.")
    print(f"Categorias antes de crear: {Categorias.objects.all()}")
    response = client.post(reverse('categories:manage'), data)
    print(f"Categorias después de crear: {Categorias.objects.all()}")

    assert Categorias.objects.get(nombre_categoria='Categoría de prueba'), 'La categoría no se ha creado correctamente.'
    assert response.status_code == 302, 'No se ha redirigido correctamente tras crear la categoría.'
    
    # Verificar el mensaje de éxito
    # messages = list(get_messages(response.wsgi_request))
    # assert any("Categoría creada con éxito." in str(message) for message in messages), "El mensaje de éxito no se ha mostrado."


# @pytest.mark.django_db
# def test_limite_categorias_con_prioridad(client, setup):
#     """
#     Test para verificar que no se pueden crear más de 5 categorías con prioridad.
#     """
#     user, _ = setup

#     # Crear 5 categorías con prioridad
#     for i in range(5):
#         Categorias.objects.create(nombre_categoria=f'Categoría con prioridad {i+1}', prioridad=True)
    
#     data = {
#         'nombre_categoria': 'Categoría con prioridad extra',
#         'prioridad': True
#     }
    
#     response = client.post(reverse('categories:manage'), data)
    
#     # Verificar que no se ha creado la nueva categoría con prioridad
#     assert not Categorias.objects.filter(nombre_categoria='Categoría con prioridad extra', prioridad=True).exists(), "Se ha creado una categoría con prioridad cuando no debería haberse creado."
#     assert response.status_code == 200, "No se ha redirigido correctamente tras fallar la creación."
    
#     # Verificar el mensaje de error
#     messages = list(get_messages(response.wsgi_request))
#     assert any("No se pueden crear más de 5 categorías con prioridad." in str(message) for message in messages), "El mensaje de error no se ha mostrado."
