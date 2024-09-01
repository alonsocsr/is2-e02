from django import forms
from django.contrib.auth.models import Permission,User,Group
from .models import Roles

class Rol_Form(forms.ModelForm):
    """
    Formulario que define un modelo de formulario para crear o modificar roles en el sistema.

    Atributos:
    ----------
    nombre_rol : CharField
        Campo de texto para el nombre del rol, obligatorio.
    rol_por_defecto : BooleanField
        Campo booleano para marcar si el rol es por defecto, opcional.
    descripcion : CharField
        Campo de texto para la descripción del rol, opcional.
    permisos : ModelMultipleChoiceField
        Campo para seleccionar múltiples permisos asociados al rol.
    
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
        queryset=Permission.objects.all().order_by('name').filter(content_type_id=1),
        widget=forms.CheckboxSelectMultiple,
        label="Permisos a ser asignados"
    )
    
    class Meta:
        model=Roles
        fields=['nombre_rol','rol_por_defecto','descripcion','permisos']
        
    def rol_name_exists(self):
        """
        Verifica que el nombre del rol no haya sido utilizado previamente.
        
        Returns:
        --------
        str
            El nombre del rol si no existe previamente.
        
        Raises:
        -------
        ValidationError
            Si el nombre del rol ya existe en la base de datos.
        """
        
        nombre=self.cleaned_data.get('nombre_rol')
        if Roles.objects.filter(nombre_rol=nombre).exists():
            raise forms.ValidationError("Ya existe un rol con este nombre. Por favor elija otro nombre")
        
        return nombre

class Asignar_Rol_Form(forms.Form):
    """
    Clase que define un modelo de form para asignar roles a un usuario
    
    Se utiliza el ModelForm proveido por Django
    
    Atributos:
    ----------
    nombre_rol : ModelChoiceField
        Campo de selección de roles disponibles en el sistema.
    usuarios : ModelChoiceField
        Campo de selección de usuarios a quienes se les asignarán los roles.
    """
    
    nombre_rol=forms.ModelChoiceField(
        queryset=Group.objects.all().order_by('name'),
        widget=forms.Select,
        label="Roles disponibles"
    )
    
    usuarios=forms.ModelChoiceField(
        queryset=User.objects.all().order_by('first_name'),
        widget=forms.Select,
        label="Lista de Usuarios"
    )
    
        
    