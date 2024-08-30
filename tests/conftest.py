import pytest
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from permissions.models import Roles


@pytest.fixture
def setup(client):
    """
    Fixture que crea un usuario y un rol para usar en los tests
    """
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')

    permiso = Permission.objects.create(
        codename='_test', content_type_id=3, name='test permiso')

    data = {
        'nombre_rol': 'test',
        'rol_por_defecto': False,
        'descripcion': 'Este es un rol de test',
        'permisos': [permiso.id]
    }

    client.post(reverse('crear_rol'), data)
    rol_creado = Roles.objects.get(nombre_rol='test')

    return user, rol_creado