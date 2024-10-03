import sys
from django import forms
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Contenido, ContenidoReportado
from categories.models import Categorias
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class ContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = ['titulo', 'resumen', 'imagen', 'cuerpo', 'categoria', 'fecha_publicacion', 'vigencia', 'slug']
        labels = {
            'titulo': 'Titulo:',
            'resumen': 'Resumen:',
            'imagen': 'Imagen Principal:',
            'cuerpo': 'Cuerpo del Contenido:',
            'categoria': 'Categoria:',
            'fecha_publicacion': '(Opcional) Fecha de Publicación:',
            'vigencia': '(Opcional) Fecha de vigencia:',
        }
        widgets = {
            'fecha_publicacion': forms.DateInput(attrs={'type': 'date'}),
            'vigencia': forms.DateInput(attrs={'type': 'date'}),
            'slug': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        autor = kwargs.pop('autor', None)

        super(ContenidoForm, self).__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['fecha_publicacion'].required = False
        self.fields['vigencia'].required = False
        if autor.has_perm('permissions.categoria_no_moderada'):
            self.fields['categoria'].queryset = Categorias.objects.all()
        else:
            self.fields['categoria'].queryset = Categorias.objects.filter(moderada=True)
        
        # clases para el front
        self.fields['fecha_publicacion'].widget.attrs.update({
            'class': 'form-input w-full p-2 text-gray-700 bg-gray-200 rounded-md',
        })
        self.fields['vigencia'].widget.attrs.update({
            'class': 'form-input w-full p-2 text-gray-700 bg-gray-200 rounded-md',
        })
        self.fields['categoria'].widget.attrs.update({
            'class': 'form-select w-full p-2 text-gray-700 bg-gray-200 rounded-md',
        })
        if autor is not None:
            self.initial['autor'] = autor
    
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen', False)
        max_size = 2 * 1024 * 1024  # 2MB
        if imagen and imagen.size > max_size:
            raise ValidationError("El tamaño de la imagen no debe exceder los 2MB.")
        return imagen
    
    def clean_slug(self):
        instance = self.instance
        titulo = self.cleaned_data.get('titulo')
        if not titulo:
            return self.cleaned_data.get('slug', None)
        slug = slugify(titulo)
        if instance.pk and instance.slug == slug:
            return slug
        if Contenido.objects.filter(slug=slug).exists():
            self.add_error('titulo', 'Este Título ya está en uso. Elige otro.')
            return slug
        return slug

    def save(self, commit=True):
        contenido = super(ContenidoForm, self).save(commit=False)
        if 'autor' in self.initial:
            contenido.autor = self.initial['autor']
        if commit:
            contenido.save()
            contenido.save_version()
        return contenido
    
    
class EditarContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = ['resumen', 'cuerpo']
        labels = {
            'resumen': 'Resumen',
            'cuerpo': 'Cuerpo del Contenido',
        }
        widgets = {
            'usuario_editor': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        editor = kwargs.pop('usuario_editor', None)

        super(EditarContenidoForm, self).__init__(*args, **kwargs)
        if editor is not None:
            self.initial['usuario_editor'] = editor

    def save(self, commit=True):
        contenido = super(EditarContenidoForm, self).save(commit=False)
        if 'usuario_editor' in self.initial:
            contenido.usuario_editor = self.initial['usuario_editor']
        if commit:
            contenido.save()
        return contenido
    
    
class RechazarContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = ['mensaje_rechazo']
        widgets = {
            'mensaje_rechazo': forms.Textarea(attrs={'rows': 4})
        }

class ContenidoReportadoForm(forms.ModelForm):
    class Meta:
        model = ContenidoReportado
        fields = ['motivo','email']
        widgets = {
            'motivo': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.is_authenticated:
            self.fields.pop('email')