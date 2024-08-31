import pytest
from django.urls import reverse
from django.contrib.auth.models import Permission, Group
from permissions.models import Roles


@pytest.mark.django_db
def test_crear_rol(client, setup):
    """
    test que prueba la vista y la creacion de un rol
    """
    user, rol_creado = setup

    permiso = Permission.objects.create(
        codename='permiso_test', content_type_id=7, name='test permiso')

    data = {
        'nombre_rol': 'test',
        'rol_por_defecto': False,
        'descripcion': 'Este es un rol de test',
        'permisos': [permiso.id]
    }

    response = client.post(reverse('crear_rol'), data)
    # print(Roles.objects.all())

    assert Roles.objects.get(nombre_rol='test')
    assert response.status_code == 200


@pytest.mark.django_db
def test_asignar_rol_usuario(client, setup):
    """
    test que prueba la vista y la asignacion de un rol a un usuario
    """
    user, rol_creado = setup

    data = {
        'nombre_rol': Group.objects.get(name='test').id,
        'usuarios': user.id,
    }

    response = client.post(reverse('asignar_rol'), data)

    # print(user.groups.all())

    assert user.groups.get(name='test')
    assert response.status_code == 302


@pytest.mark.django_db
def test_modificar_rol(client, setup):
    user, rol_creado = setup

    Permission.objects.create(
        codename='_modificar', content_type_id=3, name='permiso añadido')

    data = {
        'nombre_rol': rol_creado.nombre_rol,
        'rol_por_defecto': False,
        'descripcion': 'Este es un rol de test',
        'permisos': [Permission.objects.get(codename='_modificar').id]
    }

    print(rol_creado.permisos.all())
    response = client.post(
        reverse('modificar_rol', args=[rol_creado.id]), data)
    print(rol_creado.permisos.all())

    assert response.status_code == 302


@pytest.mark.django_db
def test_eliminar_rol(client, setup):
    user, rol_creado = setup
    response = client.post(reverse('eliminar_rol', args=[rol_creado.id]), {})

    assert not Roles.objects.filter(nombre_rol='test').exists()
    assert response.status_code == 302
