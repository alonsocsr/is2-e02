import pytest
from django.urls import reverse
from django.contrib.auth.models import Permission, User
from content.models import Contenido
from django.utils import timezone

# @pytest.mark.django_db
# def test_autor_crea_contenido(client, setup, transactional_db):
#     """
#     Test para verificar que un autor puede crear un contenido en estado 'Borrador'.
#     """
#     user, _ = setup

#     # Asignar permiso para crear contenido
#     permiso_crear = Permission.objects.get(codename='crear_contenido')
#     user.user_permissions.add(permiso_crear)

#     # Datos del contenido
#     data = {
#         'titulo': 'Nuevo Contenido',
#         'resumen': 'Este es un resumen del contenido',
#         'cuerpo': 'Este es el cuerpo del contenido',
#         'categoria': 1,  # Asumimos que hay una categoría con id=1
#         'estado': 'Borrador',
#         'fecha_publicacion': timezone.now().date(),
#         'vigencia': timezone.now().date(),
#     }

#     # Crear el contenido
#     response = client.post(reverse('crear_contenido_nuevo'), data)

#     # Verificar que el contenido se haya creado correctamente en estado 'Borrador'
#     assert Contenido.objects.filter(titulo='Nuevo Contenido', estado='Borrador').exists(), "El contenido no se creó correctamente."
#     assert response.status_code == 302, "No se redirigió correctamente después de crear el contenido."


# @pytest.mark.django_db
# def test_autor_envia_contenido_a_edicion(client, setup, transactional_db):
#     """
#     Test para verificar que un autor puede enviar un contenido a 'Edición'.
#     """
#     user, _ = setup

#     # Crear un contenido en estado 'Borrador'
#     contenido = Contenido.objects.create(
#         titulo='Contenido en Borrador',
#         resumen='Resumen de prueba',
#         cuerpo='Cuerpo de prueba',
#         autor=user,
#         estado='Borrador',
#         categoria_id=1
#     )

#     # El autor envía el contenido a edición
#     response = client.post(reverse('cambiar_estado', args=[contenido.pk]), {'estado': 'Edicion'})

#     # Verificar que el contenido se haya enviado a 'Edición'
#     contenido.refresh_from_db()
#     assert contenido.estado == 'Edicion', "El contenido no se ha enviado a Edición correctamente."
#     assert response.status_code == 302, "No se redirigió correctamente después de enviar el contenido a Edición."


# @pytest.mark.django_db
# def test_editor_envia_contenido_a_publicacion(client, setup, transactional_db):
#     """
#     Test para verificar que un editor puede enviar un contenido a 'Publicación'.
#     """
#     user, _ = setup

#     # Asignar permiso de editor para el usuario
#     permiso_editar = Permission.objects.get(codename='editar_contenido')
#     user.user_permissions.add(permiso_editar)

#     # Crear un contenido en estado 'Edicion'
#     contenido = Contenido.objects.create(
#         titulo='Contenido en Edición',
#         resumen='Resumen de prueba',
#         cuerpo='Cuerpo de prueba',
#         autor=user,
#         estado='Edicion',
#         categoria_id=1
#     )

#     # El editor envía el contenido a publicación
#     response = client.post(reverse('cambiar_estado', args=[contenido.pk]), {'estado': 'Publicar'})

#     # Verificar que el contenido se haya enviado a 'Publicar'
#     contenido.refresh_from_db()
#     assert contenido.estado == 'Publicar', "El contenido no se ha enviado a Publicación correctamente."
#     assert response.status_code == 302, "No se redirigió correctamente después de enviar el contenido a Publicación."


# @pytest.mark.django_db
# def test_publicador_publica_contenido(client, setup):
#     """
#     Test para verificar que un publicador puede publicar un contenido.
#     """
#     user, _ = setup

#     # Asignar permiso de publicador para el usuario
#     permiso_publicar = Permission.objects.get(codename='publicar_contenido')
#     user.user_permissions.add(permiso_publicar)

#     # Crear un contenido en estado 'Publicar'
#     contenido = Contenido.objects.create(
#         titulo='Contenido para Publicar',
#         resumen='Resumen de prueba',
#         cuerpo='Cuerpo de prueba',
#         autor=user,
#         estado='Publicar',
#         categoria_id=1
#     )

#     # El publicador publica el contenido
#     response = client.post(reverse('cambiar_estado', args=[contenido.pk]), {'estado': 'Publicado'})

#     # Verificar que el contenido se haya publicado
#     contenido.refresh_from_db()
#     assert contenido.estado == 'Publicado', "El contenido no se ha publicado correctamente."
#     assert contenido.activo is True, "El contenido debería estar activo después de ser publicado."
#     assert response.status_code == 302, "No se redirigió correctamente después de publicar el contenido."
