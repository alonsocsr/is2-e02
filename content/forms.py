from django import forms
from .models import Contenido
from categories.models import Categorias

class ContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = ['titulo', 'imagen', 'cuerpo', 'categoria']
        labels = {
            'titulo': 'Titulo',
            'imagen': 'Selecciona una Imagen',
            'cuerpo': 'Cuerpo del Contenido',
            'categoria': 'Categoria',
        }
        widgets = {
            'autor': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        autor = kwargs.pop('autor', None)

        super(ContenidoForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categorias.objects.all()
        if autor is not None:
            self.initial['autor'] = autor

    def save(self, commit=True):
        contenido = super(ContenidoForm, self).save(commit=False)
        if 'autor' in self.initial:
            contenido.autor = self.initial['autor']
        if commit:
            contenido.save()
        return contenido