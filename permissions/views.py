from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .models import Roles
from .forms import Rol_Form, Asignar_Rol_Form
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.


@login_required
@permission_required('permissions.crear_rol', raise_exception=True)
def crear_rol(request):
    """
    Función que se encarga de crear un nuevo rol utilizando los datos proporcionados en el formulario Rol_Form.

    Renderiza la plantilla 'permissions/crear_rol.html' con el formulario y la lista de roles existentes.

    Parámetros:
    -----------
    request : HttpRequest
        La solicitud HTTP recibida por la vista.

    Returns:
    --------
    HttpResponse
        La respuesta HTTP que renderiza la plantilla 'permissions/crear_rol.html'.
    """
    if request.method == 'POST':
        form = Rol_Form(request.POST)
        if form.is_valid():
            rol = form.save()
            permisos = rol.obtener_permisos()
            rol.asginar_permisos_rol(permisos)
            messages.success(request, f'El rol {rol.nombre_rol} ha sido creado exitosamente.')
            return redirect('crear_rol')
    else:
        form = Rol_Form()
    
    roles = Roles.objects.all().order_by('id')

    context = {
        'form': form,
        'roles': roles,
        'action': 'crear'
    }

    if request.user.is_authenticated:
        return render(request, 'permissions/crear_rol.html', context)
    else:
        return HttpResponseNotFound()


@login_required
@permission_required('permissions.asignar_rol', raise_exception=True)
def asignar_rol_usuario(request):
    """
    Función que se encarga de asignar un rol a un usuario seleccionado utilizando el formulario Asignar_Rol_Form.

    Renderiza la plantilla 'permissions/asignar_rol.html' con el formulario para asignar roles.

    Parámetros:
    -----------
    request : HttpRequest
        La solicitud HTTP recibida por la vista.

    Returns:
    --------
    HttpResponse
        La respuesta HTTP que renderiza la plantilla 'permissions/asignar_rol.html'.
    """    
    form = Asignar_Rol_Form(request.POST or None)

    context = {
        'user': request.user,
        'form': form
    }
    if request.POST:
        if form.is_valid():
            """
            se obtienen los datos del formulario
            """
            group = form.cleaned_data["nombre_rol"]
            usuario = form.cleaned_data["usuarios"]

            """
            Se asigna al usuario el rol seleccionado, antes se chequea que ya no posea ese rol
            """
            if group in usuario.groups.all():
                messages.success(
                    request, f'El usuario {usuario} ya posee el rol {group.name}')
                return render(request, 'permissions/asignar_rol.html', context)
            else:
                usuario.groups.add(group)

                permisos = group.permissions.all()
                for permiso in permisos:
                    usuario.user_permissions.add(permiso)

                usuario.save()

                messages.success(
                    request, f'Ha sido asignado el rol {group.name} a {usuario}')
                return redirect('asignar_rol')
        else:
            form = Asignar_Rol_Form()

    context = {
        'user': request.user,
        'form': form
    }
    if request.user.is_authenticated:
        return render(request, 'permissions/asignar_rol.html', context)
    else:
        return HttpResponseNotFound()


@login_required
@permission_required('permissions.modificar_rol', raise_exception=True)
def modificar_rol(request, rol_id=None):
    """
    Función que se encarga de modificar un rol.
    
    Renderiza la plantilla 'permissions/modificar_rol.html' y permite al usuario modificar un rol existente.
    
    Parámetros:
    -----------
    request : HttpRequest
        La solicitud HTTP recibida por la vista.
    rol_id : int, opcional
    
    Returns:
    --------
    HttpResponse
        La respuesta HTTP que renderiza la plantilla 'permissions/modificar_rol.html'.
    """

    rol_seleccionado = get_object_or_404(Roles, id=rol_id)
    
    if request.method == 'POST':
        form = Rol_Form(request.POST, instance=rol_seleccionado)
        if form.is_valid():
            form.save()
            messages.success(request, f'El rol {rol_seleccionado.nombre_rol} ha sido actualizado.')
            return redirect('crear_rol')
    else:
        form = Rol_Form(instance=rol_seleccionado)
    
    # Mantener todos los roles para mostrar en la tabla
    roles = Roles.objects.all().order_by('id')

    context = {
        'form': form,
        'roles': roles,  # Asegura que todos los roles siguen estando en el contexto
        'rol_seleccionado': rol_seleccionado,
        'action': 'modificar'
    }
    return render(request, 'permissions/crear_rol.html', context)


@login_required
@permission_required('permissions.eliminar_rol', raise_exception=True)
def eliminar_rol(request, rol_id):
    """
    Función que se encarga de eliminar un rol y su grupo asociado.

    Renderiza el template 'permissions/eliminar_rol.html' y muestra un mensaje de exito si el rol se elimina correctamente.

    Parámetros:
    -----------
    request : HttpRequest
        La solicitud HTTP recibida.
    rol_id : int
        El ID del rol a eliminar.

    Returns:
    --------
    HttpResponseRedirect
        Redirecciona a la vista 'crear_rol' después de eliminar el rol.

    """

    rol = get_object_or_404(Roles, id=rol_id)
    group = Group.objects.get(name=rol)
    if request.method == 'POST':
        rol.delete()
        group.delete()
        messages.success(
            request, f'El rol {rol.nombre_rol} ha sido eliminado exitosamente.')
        return redirect('crear_rol')

    context = {
        'rol': rol
    }
    return render(request, 'permissions/eliminar_rol.html', context)



@login_required
@permission_required('permissions.asignar_rol', raise_exception=True)
def modificar_usuario(request, user_id=None):
    """
    Función que se encarga de modificar los roles de un usuario.

    Renderiza el template 'permissions/modificar_usuario.html' y actualiza los roles del usuario seleccionado.

    Parámetros:
    -----------
    request : HttpRequest
        La solicitud HTTP recibida.
    user_id : int, opcional
        El ID del usuario cuyos roles se desean modificar. Por defecto es None.

    Returns:
    --------
    HttpResponse
        La respuesta HTTP que renderiza el template 'permissions/modificar_usuario.html'.
    """
    usuarios = User.objects.all()
    roles = Group.objects.all()

    if user_id:

        usuario_seleccionado = get_object_or_404(User, id=user_id)
        roles_usuario = usuario_seleccionado.groups.all()

        if request.method == "POST":
            # obtener los roles seleccionados en el formulario
            roles_seleccionados = request.POST.getlist('roles')

            for rol in roles:
                if str(rol.id) in roles_seleccionados:
                    if rol.name != 'Suscriptor' or rol in roles_usuario:
                        # si el rol seleccionado no es suscriptor o si el rol ya esta asignado
                        if rol not in usuario_seleccionado.groups.all():
                            # si el rol no esta asignado se asigna
                            usuario_seleccionado.groups.add(rol)
                else:
                    if rol.name != 'Suscriptor' and rol in usuario_seleccionado.groups.all():
                        # todo rol no seleccionado que no sea suscriptor se elimina
                        usuario_seleccionado.groups.remove(rol)

            messages.success(
                request, f'Se han actualizado los roles del usuario {usuario_seleccionado.username}.')
            return redirect('modificar_usuario', user_id=user_id)
    else:
        usuario_seleccionado = None
        roles_usuario = None

    context = {
        'usuarios': usuarios,
        'roles': roles,
        'usuario_seleccionado': usuario_seleccionado,
        'roles_usuario': roles_usuario,
    }

    return render(request, 'permissions/modificar_usuario.html', context)