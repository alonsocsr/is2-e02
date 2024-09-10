import pytest
from django.urls import reverse
from django.contrib.auth.models import Permission, Group, User
from permissions.models import Roles


@pytest.mark.django_db
def test_crear_rol(client, monkeypatch):
    """
    test que prueba la vista y la creacion de un rol
    """
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')

    monkeypatch.setattr('django.contrib.auth.decorators.permission_required',
                         lambda perm, *args, **kwargs: lambda view: view) 

    permiso = Permission.objects.create(
        codename='permiso_test', content_type_id=1, name='test permiso')

    data = {
        'nombre_rol': 'test',
        'rol_por_defecto': False,
        'descripcion': 'Este es un rol de test',
        'permisos': [permiso.id]
    }

    print(f"\n\nProbando la creación del rol test.")
    print(f"Roles inicialmente:             {Roles.objects.all()}")
    response = client.post(reverse('crear_rol'), data)
    print(f"Roles después de la creación:   {Roles.objects.all()}")
    print(f"Redirección correcta. Http response {response.status_code}")


    assert Roles.objects.get(nombre_rol='test'), 'No se ha creado el rol'
    assert response.status_code == 302, 'No se ha redirigido correctamente tras crear la categoría.'

@pytest.mark.django_db
def test_asignar_rol_usuario(client, setup):
    """
    test que prueba la vista y la asignacion de un rol a un usuario
    """
    user, _ = setup

    data = {
        'nombre_rol': Group.objects.get(name='test_rol').id,
        'usuarios': user.id,
    }

    print(f"\n\nProbando la asignación del rol test_rol al usuario {user.username}.")
    print(f"Roles del usuario inicialmente:                 {user.groups.all()}")
    response = client.post(reverse('asignar_rol'), data)
    print(f"Roles del usuario después de la asignación:     {user.groups.all()}")
    print(f"Redirección correcta. Http response {response.status_code}")

    assert user.groups.get(name='test_rol'), 'No se ha asignado el rol'
    assert response.status_code == 302, 'La redirección no es correcta'


@pytest.mark.django_db
def test_modificar_rol(client, setup):
    _, rol_creado = setup

    Permission.objects.create(
        codename='añadir', content_type_id=1, name='permiso añadido')

    data = {
        'nombre_rol': rol_creado.nombre_rol,
        'rol_por_defecto': False,
        'descripcion': 'Este es un rol de test',
        'permisos': [Permission.objects.get(codename='añadir').id]
    }

    print(f"\n\nProbando la modificación del rol test_rol.")
    print(f"Permisos del rol inicialmente:                 {rol_creado.permisos.all()}")
    response = client.post(reverse('modificar_rol', args=[rol_creado.id]), data)
    print(f"Permisos del rol después de la modificación:   {rol_creado.permisos.all()}")
    print(f"Redirección correcta. Http response {response.status_code}")

    assert response.status_code == 302, 'La redirección no es correcta'


@pytest.mark.django_db
def test_eliminar_rol(client, setup):
    _, rol_creado = setup

    print(f"\n\nProbando la eliminación del rol test_rol.")
    print(f"Roles inicialmente:                 {Roles.objects.all()}")
    response = client.post(reverse('eliminar_rol', args=[rol_creado.id]), {})
    print(f"Roles después de la eliminación:    {Roles.objects.all()}")
    print(f"Redirección correcta. Http response {response.status_code}")

    assert not Roles.objects.filter(nombre_rol='test_rol').exists(), 'El rol no se ha eliminado'
    assert response.status_code == 302, 'La redirección no es correcta'
