from django import forms
from .models import Categorias, TIPO_CATEGORIA_OPCIONES

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = ['nombre_categoria', 'descripcion', 'descripcion_corta', 'moderada', 'tipo_categoria']

    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        self.fields['nombre_categoria'].widget.attrs.update({
            'class': 'form-input w-full p-2 text-gray-700 bg-gray-200 rounded-md'
        })
        self.fields['descripcion'].widget.attrs.update({
            'class': 'form-textarea w-full p-2 text-gray-700 bg-gray-200 rounded-md',
            'style': 'height: 80px; overflow-y: auto; resize: none;'
        })
        self.fields['descripcion_corta'].widget.attrs.update({
            'class': 'form-input w-full p-2 text-gray-700 bg-gray-200 rounded-md'
        })
        self.fields['moderada'].widget.attrs.update({
            'class': 'form-checkbox text-gray-700 bg-gray-200 rounded',
        })
        self.fields['tipo_categoria'].widget.attrs.update({
            'class': 'form-select w-full p-2 text-gray-700 bg-gray-200 rounded-md',
        })
        # Establecer valor inicial para "moderada" si no está definido
        if 'moderada' not in self.initial:
            self.initial['moderada'] = True
