from django import forms
from .models import TIPO_CATEGORIA_OPCIONES

class CategoriaForm(forms.Form):
    nombre_categoria = forms.CharField(
        max_length=30,
        label='Nombre de la Categoría',
        widget=forms.TextInput(attrs={
            'class': 'form-input w-full p-2 text-gray-700 bg-gray-200 rounded-md'
        })
    )

    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-textarea w-full p-2 text-gray-700 bg-gray-200 rounded-md',
            'style': 'height: 80px; overflow-y: auto; resize: none;'
        }),
        max_length=100,
        label='Descripción'
    )

    descripcion_corta = forms.CharField(
        max_length=10,
        label='Descripción Corta',
        widget=forms.TextInput(attrs={
            'class': 'form-input w-full p-2 text-gray-700 bg-gray-200 rounded-md'
        })
    )

    moderada = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox text-gray-700 bg-gray-200 rounded',
        }),
        label='Moderada',
        initial=True
    )

    tipo_categoria = forms.ChoiceField(
        choices=TIPO_CATEGORIA_OPCIONES,
        widget=forms.Select(attrs={
            'class': 'form-select w-full p-2 text-gray-700 bg-gray-200 rounded-md',
        }),
        label='Tipo de Categoría'
    )
