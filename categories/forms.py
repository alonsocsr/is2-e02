from django import forms
from .models import Categorias, TIPO_CATEGORIA_OPCIONES
from django.core.exceptions import ValidationError

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = ['nombre_categoria', 'descripcion', 'descripcion_corta', 'moderada', 'prioridad', 'tipo_categoria']

    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        self.fields['nombre_categoria'].widget.attrs.update({
            'class': 'w-full text-sm px-4 py-3 bg-gray-200 focus:bg-gray-100 border border-gray-200 rounded-lg focus:outline-none focus:border-pink-400',
            'placeholder': 'Nombre de la categoría'
        })
        self.fields['descripcion'].widget.attrs.update({
            'class': 'w-full text-sm px-4 py-3 bg-gray-200 focus:bg-gray-100 border border-gray-200 rounded-lg focus:outline-none focus:border-pink-400',
            'style': 'resize: none; height: 80px;',
            'placeholder': 'Descripcion larga'
        })
        self.fields['descripcion_corta'].widget.attrs.update({
            'class': 'w-full text-sm px-4 py-3 bg-gray-200 focus:bg-gray-100 border border-gray-200 rounded-lg focus:outline-none focus:border-pink-400',
            'placeholder': 'Descripción corta'
        })
        self.fields['moderada'].widget.attrs.update({
            'class': 'form-checkbox text-gray-700 bg-gray-200 rounded',
        })
        self.fields['prioridad'].widget.attrs.update({
            'class': 'form-checkbox text-gray-700 bg-gray-200 rounded',
        })
        self.fields['tipo_categoria'].widget.attrs.update({
            'class': 'form-select w-full text-sm px-4 py-3 bg-gray-200 focus:bg-gray-100 border border-gray-200 rounded-lg focus:outline-none focus:border-pink-400',
        })
        # Establecer valor inicial para "moderada" si no está definido
        if 'moderada' not in self.initial:
            self.initial['moderada'] = True
