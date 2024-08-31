import pytest
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from permissions.models import Roles, Group


@pytest.fixture
def setup(client):
    """
    Fixture que crea un usuario y un rol para usar en los tests
    """
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')

    permiso = Permission.objects.create(
        codename='test', content_type_id=1, name='test permiso')

    data = {
        'nombre_rol': 'test_rol',
        'rol_por_defecto': False,
        'descripcion': 'Este es un rol de test',
        'permisos': [permiso.id]
    }
    print(Roles.objects.all())
    print(Group.objects.all())

    response = client.post(reverse('crear_rol'), data)
    rol_creado = Roles.objects.get(nombre_rol='test_rol')

    print(Roles.objects.all())
    print(Group.objects.all())

    return user, rol_creado
