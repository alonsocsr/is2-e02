import pytest
from django.urls import reverse
from django.contrib.auth.models import User, Group


def test_home(client, transactional_db):
    response = client.get(reverse("home"))
    print(f"\n\nProbando la vista home.")
    print(f"Ingreso correcto. Http response {response.status_code}")
    assert response.status_code == 200


@pytest.mark.parametrize("correo, username, contraseña, valido", [
    ("test@test.com", "testuser", "Valido123!", True),          # Caso válido
    ("test@test.com", "testuser", "corto", False),              # Contraseña demasiado corta
    ("test@test.com", "testuser", "", False),                   # Contraseña vacía
    ("not-an-email", "testuser", "Valido123!", False),])        # Email inválido
def test_signup(client, correo, username, contraseña, valido, transactional_db):
    """
    Test de signup que valida diferentes combinaciones de email, username y password.
    """
    Group.objects.get_or_create(name='Suscriptor')

    data = {
        'email': correo,
        'username': username,
        'password1': contraseña,
        'password2': contraseña,

    }

    print(
        f"\nProbando el registro de un usuario con email {correo} y contraseña {contraseña}.")
    response = client.post(reverse('account_signup'), data)

    if valido:
        assert User.objects.filter(username=username).exists()
        assert response.status_code == 302
    else:
        assert not User.objects.filter(username=username).exists()
        assert response.status_code == 200
