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
            # return render(request, 'home/home.html')
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
                usuario.save()

            messages.success(
                request, f'Ha sido asignado el rol {group.name} a {usuario}')
            return render(request, 'home/home.html')
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
    Funcion que se encarga de modificar un rol que no sea por defectotomando los datos del formulario de Rol_Form
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
    group=Group.objects.get(name=rol)
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