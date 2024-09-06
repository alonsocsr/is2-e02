from django import forms
from .models import Contenido
from categories.models import Categorias
from django.utils.text import slugify

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
            'fecha_publicacion': 'Fecha de Publicación:',
            'vigencia': 'Fecha de vigencia:',
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
        self.fields['categoria'].queryset = Categorias.objects.all()
        if autor is not None:
            self.initial['autor'] = autor
        
    def clean_slug(self):
        instance = self.instance
        slug = slugify(self.cleaned_data['titulo'])
        if instance.pk and instance.slug == slug:
            return slug
        if Contenido.objects.filter(slug=slug).exists():
            raise forms.ValidationError('Este Título ya está en uso. Elige otro.')
        return slug

    def save(self, commit=True):
        contenido = super(ContenidoForm, self).save(commit=False)
        if 'autor' in self.initial:
            contenido.autor = self.initial['autor']
        if commit:
            contenido.save()
            contenido.save_version()
        return contenido