import pytest
from django.urls import reverse
from categories.models import Categorias
from django.contrib.messages import get_messages


@pytest.mark.django_db
def test_crear_categoria(client, setup):
    """
    Test para verificar que se puede crear una categoría.
    """

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


@pytest.mark.django_db
def test_limite_categorias_con_prioridad(client, setup):
    """
    Test para verificar que no pueden haber más de 5 categorías con prioridad.
    """

    for i in range(5):
        Categorias.objects.create(nombre_categoria=f'CatP {i+1}', prioridad=True)
    
    data = {
        'nombre_categoria': 'CatP 6',
        'descripcion': 'Cat con prioridad 6',
        'descripcion_corta': 'Corta',
        'tipo_categoria': 'PU',
        'prioridad': True
    }
    
    print(f"\n\nProbando el límite de categorias con prioridad.")
    print(f"Categorias antes de crear: {Categorias.objects.all()}")
    response = client.post(reverse('categories:manage'), data)
    print(f"Categorias después de crear: {Categorias.objects.all()}")
    print("mensaje:")
    messages = list(get_messages(response.wsgi_request))
    for message in messages:
        if ("No se pueden crear más de 5 categorías con prioridad." in str(message)):
            print(f"     {message}")
   

    assert not Categorias.objects.filter(nombre_categoria='CatP 8', prioridad=True).exists(), "Se ha creado una categoría con prioridad cuando no debería haberse creado."
    assert response.status_code == 200, "No se ha redirigido correctamente tras fallar la creación."
    
@pytest.mark.django_db
def test_modificar_categoria(client, setup):
    """
    Test para verificar que se puede modificar una categoría existente.
    """

    categoria = Categorias.objects.create(nombre_categoria='Categoría inicial')
    
    data = {
        'nombre_categoria': 'Categoría modificada',
        'descripcion': 'Descripción de prueba',
        'descripcion_corta': 'Corta',
        'tipo_categoria': 'PU'
    }

    print(f"\n\nProbando la modificación de la categoría.")
    print(f"Categoría antes de modificar: {categoria}")
    response = client.post(reverse('categories:modificar', args=[categoria.pk]), data)
    categoria.refresh_from_db()
    print(f"Categoría después de modificar: {categoria}")
    print("mensaje:")
    messages = list(get_messages(response.wsgi_request))
    for message in messages:
        if ("Categoría modificada con éxito." in str(message)):
            print(f"     {message}")

    assert categoria.nombre_categoria == 'Categoría modificada', "La categoría no se ha modificado correctamente."
    assert response.status_code == 302, "No se ha redirigido correctamente después de modificar la categoría."


@pytest.mark.django_db
def test_eliminar_categoria(client, setup):
    """
    Test para verificar que se puede eliminar una categoría existente.
    """

    categoria = Categorias.objects.create(nombre_categoria='Categoría a eliminar', prioridad=False)

    print(f"\n\nProbando la eliminación de la categoría.")
    print(f"Categorías antes de eliminar: {Categorias.objects.all()}")
    response = client.post(reverse('categories:eliminar', args=[categoria.pk]))
    print(f"Categorías después de eliminar: {Categorias.objects.all()}")
    print("mensaje:")
    messages = list(get_messages(response.wsgi_request))
    for message in messages:
        if ("Categoría eliminada con éxito" in str(message)):
            print(f"     {message}")

    # Verificar que la categoría se ha eliminado correctamente
    assert not Categorias.objects.filter(pk=categoria.pk).exists(), "La categoría no se ha eliminado correctamente."
    assert response.status_code == 302, "No se ha redirigido correctamente después de eliminar la categoría."