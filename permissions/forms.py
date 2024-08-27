from django import forms
from django.contrib.auth.models import Permission
from .models import Roles

class Rol_Form(forms.ModelForm):
    """
    Clase que define un modelo de form para roles
    Se utiliza el ModelForm proveido por Django
    """
    
    nombre_rol=forms.CharField(
        max_length=50,
        required=True,
        label='Nombre del Rol'
    )
    rol_por_defecto=forms.BooleanField(initial=False,required=False)
    descripcion=forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='Ingrese la descripcion del Rol'
    )
    
    permisos=forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        label="Permisos a ser asignados"
    )
    
    class Meta:
        model=Roles
        fields=['nombre_rol','rol_por_defecto','descripcion','permisos']
        
    def rol_name_exists(self):
        """
        Funcion que comprueba que el nombre del rol a ser creado no haya sido utilizado
        return: el nombre del rol, Excepction: el nombre del rol ya existe
        """
        
        nombre=self.cleaned_data.get('nombre_rol')
        if Roles.objects.filter(nombre_rol=nombre).exists():
            raise forms.ValidationError("Ya existe un rol con este nombre. Por favor elija otro nombre")
        
        return nombre
        