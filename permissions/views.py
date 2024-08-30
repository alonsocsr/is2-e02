from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .models import Roles
from .forms import Rol_Form, Asignar_Rol_Form
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def crear_rol(request):
    """
    Funcion que se encarga de crear un rol tomando los datos del formulario de Rol_Form
    params: request
    return:render(request,'path de retorno',contexto)
    """
    form = Rol_Form(request.POST or None)
    roles = Roles.objects.all()

    if request.POST:
        if form.is_valid():
            rol = form.save()

            rol.save()

            permisos = rol.obtener_permisos()
            rol.asginar_permisos_rol(permisos)

            messages.success(
                request, f'Ha sido creado el rol {rol.nombre_rol}')

        else:
            form = Rol_Form()

    context = {
        'user': request.user,
        'form': form,
        'roles': roles
    }

    if request.user.is_authenticated:
        return render(request, 'permissions/crear_rol.html', context)
    else:
        return HttpResponseNotFound()


@login_required
def asignar_rol_usuario(request):
    """
    Funcion que se encarga de asignar un rol tomando los datos del formulario de Asignar_Rol_Form
    params: request
    return:render(request,'path de retorno',contexto)
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
def modificar_rol(request, rol_id=None):
    """
    Funcion que se encarga de modificar un rol que no sea por defecto tomando los datos del formulario de Rol_Form
    params: request, rol_id
    return:render(request,'path de retorno',contexto)
    """
    roles = Roles.objects.exclude(rol_por_defecto=True)

    if rol_id:
        rol_seleccionado = get_object_or_404(Roles, id=rol_id)
        form = Rol_Form(request.POST or None, instance=rol_seleccionado)

        if request.method == "POST" and form.is_valid():
            form.save()
            messages.success(
                request, f'El rol {rol_seleccionado.nombre_rol} ha sido actualizado.')
            return redirect('modificar_rol', rol_id=rol_id)
    else:
        rol_seleccionado = None
        form = Rol_Form()

    context = {
        'roles': roles,
        'form': form,
        'rol_seleccionado': rol_seleccionado,
    }
    return render(request, 'permissions/modificar_rol.html', context)


@login_required
def eliminar_rol(request, rol_id):
    """
    Funcion que se encarga de eliminar un rol tomando los datos del formulario de Rol_Form
    params: request, rol_id
    return:render(request,'path de retorno',contexto)
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
def modificar_usuario(request, user_id=None):
    """
    Funcion que se encarga de modificar un usuario tomando los datos del formulario de Asignar_Rol_Form
    params: request, user_id
    return:render(request,'path de retorno',contexto)
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
