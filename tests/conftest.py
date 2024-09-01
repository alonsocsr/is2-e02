import pytest
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from permissions.models import Roles


@pytest.fixture(scope='function')
def setup(client, monkeypatch):
    """
    Fixture que crea un usuario y un rol para usar en los tests
    """

    monkeypatch.setattr('django.contrib.auth.decorators.permission_required',
                        lambda perm, *args, **kwargs: lambda view: view)

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

    client.post(reverse('crear_rol'), data)
    rol_creado = Roles.objects.get(nombre_rol='test_rol')

    return user, rol_creado
