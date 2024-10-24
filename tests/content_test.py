import pytest
from django.urls import reverse
from django.contrib.auth.models import Permission,User
from content.models import Contenido
from categories.models import Categorias
from django.utils import timezone
from datetime import timedelta
import tempfile
from django.test import RequestFactory, TestCase,Client
from unittest import TestCase
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from content.views import EditarContenido
@pytest.mark.django_db
def test_autor_crea_contenido(client, setup, transactional_db):
    """
    Test para verificar que un autor puede crear un contenido en estado 'Borrador'.
    """
    user, _ = setup

  
    permiso_crear = Permission.objects.get(codename='crear_contenido')
    user.user_permissions.add(permiso_crear)
    client.force_login(user)

    categoria=Categorias.objects.create(nombre_categoria="TestCategoria")
    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp_img:
        
        image = Image.new('RGB', (100, 100), color='red')
        image.save(tmp_img, format='JPEG')
        tmp_img.seek(0)  

        image_file = SimpleUploadedFile(tmp_img.name, tmp_img.read(), content_type='image/jpeg')
    
    print(f'Contenidos antes de la creacion {Contenido.objects.all()}')    
    data = {
        'titulo': 'Nuevo Contenido', 
        'resumen': 'Este es un resumen del contenido', 
        'cuerpo': '<p>Este es el cuerpo del contenido</p>',  
        'categoria': categoria.id,   
        'estado': 'Borrador',  
        'fecha_publicacion': timezone.now().date(),  
        'vigencia': timezone.now().date() + timedelta(days=30), 
        'slug': 'nuevo-contenido',
        'imagen':image_file
    }


    response = client.post(reverse('crear_contenido_nuevo'), data)

    
    if response.status_code == 200: 
        print("Form Errors:", response.context_data['form'].errors)
        for field, errors in response.context_data['form'].errors.items():
            print(f"Error in {field}: {errors}")

    assert Contenido.objects.filter(titulo='Nuevo Contenido', estado='Borrador').exists(), "El contenido no se creó correctamente."
    print(f'Contenidos luego de la creacion {Contenido.objects.all()}')  
    assert response.status_code == 302, "No se redirigió correctamente después de crear el contenido."




@pytest.mark.django_db
def test_redireccion_lista_borradores(setup, client):

    user, rol_creado = setup
    
    permiso_borradores = Permission.objects.get(codename='crear_contenido')  
    user.user_permissions.add(permiso_borradores)
    
  
    url = reverse('lista_borradores')
    response = client.get(url)
    
    assert response.status_code == 200  
   

@pytest.mark.django_db
def test_redireccion_vista_editor(setup, client):
    user, rol_creado = setup
    
    permiso_editor = Permission.objects.get(codename='editar_contenido') 
    user.user_permissions.add(permiso_editor)
    
    url = reverse('vista_editor')
    response = client.get(url)
    
    assert response.status_code == 200
    

@pytest.mark.django_db
def test_redireccion_publicar(setup, client):
    user, rol_creado = setup
    
    permiso_publicar = Permission.objects.get(codename='publicar_contenido') 
    user.user_permissions.add(permiso_publicar)
    
    url = reverse('vista_publicador')
    response = client.get(url)
    
    assert response.status_code == 200,print(f'Acceso correcto a publicacion de contenido')
    assert 'publicar' in response.content.decode()

@pytest.mark.django_db
def test_redireccion_inactivar_contenido(setup, client):
    user, rol_creado = setup
    
    print(f'Contenidos antes de la inactivacion {Contenido.objects.all()}')  
    categoria = Categorias.objects.create(nombre_categoria="TestCategoria")
    contenido = Contenido.objects.create(
        titulo='Nuevo Contenido',
        resumen='Este es un resumen del contenido',
        cuerpo='<p>Este es el cuerpo del contenido</p>',
        categoria=categoria,
        estado='Publicado',
        activo=True,
        fecha_publicacion=timezone.now().date(),
        vigencia=timezone.now().date() + timezone.timedelta(days=30),
        slug='nuevo-contenido',
        usuario_editor=user 
    )
    

    permiso_inactivar = Permission.objects.get(codename='inactivar_contenido')
    user.user_permissions.add(permiso_inactivar)
    

    url = reverse('inactivar_contenido', kwargs={'pk': contenido.pk})
    response = client.post(url, follow=True)
    

    contenido.refresh_from_db() 
    assert response.status_code == 200
    assert contenido.activo is False  
    assert contenido.estado == 'Inactivo',print(f'Contenidos luego de la inactivacion {Contenido.objects.all()}')  
    

@pytest.mark.django_db
def test_redireccion_vista_all_contenidos(setup, client):
    user, rol_creado = setup
    
    
    
    url = reverse('vista_all_contenidos')
    response = client.get(url)
    
    assert response.status_code == 200,print(f'Acceso correcto a contenidos')
    assert 'contenidos' in response.content.decode()



@pytest.mark.django_db
def test_redireccion_detalle_contenido(setup, client):
    user, rol_creado = setup
    
    categoria = Categorias.objects.create(nombre_categoria="TestCategoria")
    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp_img:
        
        image = Image.new('RGB', (100, 100), color='red')
        image.save(tmp_img, format='JPEG')
        tmp_img.seek(0)  

        image_file = SimpleUploadedFile(tmp_img.name, tmp_img.read(), content_type='image/jpeg')
    contenido = Contenido.objects.create(
        titulo='Detalle Contenido Test',
        resumen='Este es un resumen del contenido',
        cuerpo='<p>Este es el cuerpo del contenido</p>',
        categoria=categoria,
        estado='Publicado',
        activo=True,
        fecha_publicacion=timezone.now().date(),
        vigencia=timezone.now().date() + timezone.timedelta(days=30),
        slug='detalle-contenido',
        usuario_editor=user,
        imagen=image_file 
    )

    
    url = reverse('detalle_contenido', kwargs={'slug': contenido.slug})
    response = client.get(url)
    
    assert response.status_code == 200,print(f'Acceso correcto a detalle de contenido')
    assert contenido.titulo in response.content.decode()

@pytest.mark.django_db
def test_redireccion_rechazar_contenido(setup, client):
    user, rol_creado = setup
    
    
    categoria = Categorias.objects.create(nombre_categoria="TestCategoria")
    contenido = Contenido.objects.create(
        titulo='Nuevo Contenido',
        resumen='Este es un resumen del contenido',
        cuerpo='<p>Este es el cuerpo del contenido</p>',
        categoria=categoria,
        estado='A Publicar',
        activo=False,
        fecha_publicacion=timezone.now().date(),
        vigencia=timezone.now().date() + timezone.timedelta(days=30),
        slug='nuevo-contenido',
        usuario_editor=user 
    )
    

    permiso_rechazar = Permission.objects.get(codename='rechazar_contenido')
    user.user_permissions.add(permiso_rechazar)
    

    url = reverse('rechazar_contenido', kwargs={'pk': contenido.pk})
    response = client.post(url, follow=True)
    

    contenido.refresh_from_db() 
    assert response.status_code == 200,print(f'Acceso a rechazo de contenido')
    assert contenido.activo is False  
    assert contenido.estado == 'A Publicar'  

@pytest.mark.django_db
def test_redireccion_contenidos_reportados(setup, client):
    user, rol_creado = setup
    permiso_verreportados = Permission.objects.get(codename='ver_reportes_contenido')
    user.user_permissions.add(permiso_verreportados)
    url = reverse('contenidos_reportados')
    response = client.get(url)
    
    assert response.status_code == 200,print(f'Acceso correcto a contenidos reportados')
    
@pytest.mark.django_db
def test_redireccion_contenidos_inactivos(setup, client):
    user, rol_creado = setup
    permiso_inactivo = Permission.objects.get(codename='inactivar_contenido')
    user.user_permissions.add(permiso_inactivo)
    url = reverse('contenidos_inactivados')
    response = client.get(url)
    
    assert response.status_code == 200, print(f'Acceso correcto a contenidos inactivos')
   

@pytest.mark.django_db
def test_redireccion_destacar_contenido(setup, client):
    user, rol_creado = setup
    
    categoria = Categorias.objects.create(nombre_categoria="TestCategoria")
    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp_img:
        
        image = Image.new('RGB', (100, 100), color='red')
        image.save(tmp_img, format='JPEG')
        tmp_img.seek(0)  

        image_file = SimpleUploadedFile(tmp_img.name, tmp_img.read(), content_type='image/jpeg')
    contenido = Contenido.objects.create(
        titulo='Detalle Contenido Test',
        resumen='Este es un resumen del contenido',
        cuerpo='<p>Este es el cuerpo del contenido</p>',
        categoria=categoria,
        estado='Publicado',
        activo=True,
        fecha_publicacion=timezone.now().date(),
        vigencia=timezone.now().date() + timezone.timedelta(days=30),
        slug='detalle-contenido',
        usuario_editor=user,
        imagen=image_file 
    )
    permiso_destacar = Permission.objects.get(codename='destacar_contenido')
    user.user_permissions.add(permiso_destacar)

    
    
    url = reverse('contenido_seleccionado', kwargs={'slug': contenido.slug})
    response = client.post(url, follow=True)
    
    contenido.refresh_from_db()
    assert response.status_code == 200
 
    
    
    
@pytest.mark.django_db
def test_redireccion_lista_destacados(setup, client):
    user, rol_creado = setup
    permiso_destacar = Permission.objects.get(codename='destacar_contenido')
    user.user_permissions.add(permiso_destacar)
    url = reverse('lista_destacados')
    response = client.get(url)
    
    assert response.status_code == 200

@pytest.mark.django_db
def test_compartir(client,setup):
    user, rol_creado = setup
    
     
    categoria = Categorias.objects.create(nombre_categoria="TestCategoria")
    contenido = Contenido.objects.create(
        titulo='Nuevo Contenido',
        resumen='Este es un resumen del contenido',
        cuerpo='<p>Este es el cuerpo del contenido</p>',
        categoria=categoria,
        estado='Publicado',
        activo=True,
        fecha_publicacion=timezone.now().date(),
        vigencia=timezone.now().date() + timezone.timedelta(days=30),
        slug='nuevo-contenido',
        usuario_editor=user,
        cantidad_compartidos=0
    )
    print(f'Cantidad de compartidos antes de la accion: {contenido.cantidad_compartidos}') 

    
    url = reverse('increment_share_count')
    response = client.post(url, {'contenido_id': contenido.pk}, follow=True)

    

    contenido.refresh_from_db() 
    print(f'Cantidad de compartidos luego de la accion: {contenido.cantidad_compartidos}')  
    assert response.status_code == 200  
    assert contenido.cantidad_compartidos>=1
    
@pytest.mark.django_db
def test_calificar(client,setup):
    user, rol_creado = setup
    
     
    categoria = Categorias.objects.create(nombre_categoria="TestCategoria")
    contenido = Contenido.objects.create(
        titulo='Nuevo Contenido',
        resumen='Este es un resumen del contenido',
        cuerpo='<p>Este es el cuerpo del contenido</p>',
        categoria=categoria,
        estado='Publicado',
        activo=True,
        fecha_publicacion=timezone.now().date(),
        vigencia=timezone.now().date() + timezone.timedelta(days=30),
        slug='nuevo-contenido',
        usuario_editor=user,
        cantidad_valoraciones=0
    )
    print(f'Cantidad de valoraciones antes de la accion: {contenido.cantidad_valoraciones}') 

    
    url = reverse('calificar_contenido', kwargs={'contenido_id': contenido.pk})
    response = client.post(url, {'puntuacion': 5}, follow=True)


    contenido.refresh_from_db() 
    print(f'Cantidad de valoraciones luego de la accion: {contenido.cantidad_valoraciones}')  
    assert response.status_code == 200  
    assert contenido.cantidad_valoraciones>=1
    
@pytest.mark.django_db
def test_visualizacion(client,setup):
    user, rol_creado = setup
    
    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp_img:
        
        image = Image.new('RGB', (100, 100), color='red')
        image.save(tmp_img, format='JPEG')
        tmp_img.seek(0)  

        image_file = SimpleUploadedFile(tmp_img.name, tmp_img.read(), content_type='image/jpeg')
    categoria = Categorias.objects.create(nombre_categoria="TestCategoria")
    contenido = Contenido.objects.create(
        titulo='Nuevo Contenido',
        resumen='Este es un resumen del contenido',
        cuerpo='<p>Este es el cuerpo del contenido</p>',
        categoria=categoria,
        estado='Publicado',
        activo=True,
        fecha_publicacion=timezone.now().date(),
        vigencia=timezone.now().date() + timezone.timedelta(days=30),
        slug='nuevo-contenido',
        usuario_editor=user,
        cantidad_vistas=0,
        imagen=image_file
    )
    print(f'Cantidad de vistas antes de la accion: {contenido.cantidad_vistas}') 

    
    url = reverse('detalle_contenido', kwargs={'slug': contenido.slug})
    response = client.post(url, follow=True)

    contenido.refresh_from_db() 
    print(f'Cantidad de vistas luego de la accion: {contenido.cantidad_vistas}')  
    assert response.status_code == 200  
    assert contenido.cantidad_vistas>=1