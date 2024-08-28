from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from .models import Roles
from .forms import Rol_Form,Asignar_Rol_Form
from django.contrib import messages
from django.http import HttpResponseNotFound
# Create your views here.

def crear_rol(request):
    """
    Funcion que se encarga de crear un rol tomando los datos del formulario de Rol_Form
    params: request
    return:render(request,'path de retorno',contexto)
    """
    form=Rol_Form(request.POST or None)
    
    if request.POST:
        if form.is_valid():
            rol=form.save()
            
            rol.save()
            
            permisos=rol.obtener_permisos()
            rol.asginar_permisos_rol(permisos)
            
            messages.success(request,f'Ha sido creado el rol {rol.nombre_rol}')
            return render(request, 'home/home.html')
        else:
            form=Rol_Form()
        
    context={
        'user':request.user,
        'form':form
    }
    
    if request.user.is_authenticated:
        return render(request, 'permissions/crear_rol.html',context)
    else:
        return HttpResponseNotFound()


def asignar_rol_usuario(request):
    """
    Funcion que se encarga de asignar un rol tomando los datos del formulario de Asignar_Rol_Form
    params: request
    return:render(request,'path de retorno',contexto)
    """
    form=Asignar_Rol_Form(request.POST or None)
    
    if request.POST:
        if form.is_valid():
            """
            se obtienen los datos del formulario
            """
            group=form.cleaned_data["nombre_rol"]
            usuario=form.cleaned_data["usuarios"]
            
            
            
            """
            Se asigna al usuario el rol seleccionado, antes se chequea que ya no posea ese rol
            """
            if group in usuario.groups.all():
                messages.success(request,f'El usuario {usuario} ya posee el rol {group.name}')
                return render(request, 'permissions/asignar_rol.html',context)
            else:
                usuario.groups.add(group)
                usuario.save()
                
            messages.success(request,f'Ha sido asignado el rol {group.name} a {usuario}')
            return render(request, 'home/home.html')
        else:
            form=Asignar_Rol_Form()
        
    context={
        'user':request.user,
        'form':form
    }
    if request.user.is_authenticated:
        return render(request, 'permissions/asignar_rol.html',context)
    else:
        return HttpResponseNotFound()