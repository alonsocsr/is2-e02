from django.shortcuts import render,redirect

from .models import Roles
from .forms import Rol_Form
from django.contrib import messages
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
    else:
        context={
            'error':"EL nombre del rol ya existe"
            }
        
    context={
        'user':request.user,
        'form':form
    }
    return render(request, 'permissions/crear_rol.html',context)