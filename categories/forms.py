from django import forms
from .models import TIPO_CATEGORIA_OPCIONES

class CategoriaForm(forms.Form):
    nombre_categoria = forms.CharField(
        max_length=30,
        label='Nombre de la Categoría'
    )
    
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={ 'style': 'width: 100%; height: 80px; overflow-y: auto; resize: none;',
            'class': 'form-textarea'
        }),
        max_length=100,
        label='Descripción'
    )
    
    descripcion_corta = forms.CharField(
        max_length=10,
        label='Descripción Corta'
    )
    
    moderada = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        label='Moderada',
        initial=True
    )
    
    tipo_categoria = forms.ChoiceField(
        choices=TIPO_CATEGORIA_OPCIONES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Tipo de Categoría'
    )
    
