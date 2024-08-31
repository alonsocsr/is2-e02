from django.db import models

TIPO_CATEGORIA_OPCIONES = [
    ('PU', 'Pública'),
    ('GR', 'Gratuita'),
    ('PA', 'Paga'),
]

class Categorias(models.Model):
    """
    Modelo para Categorias

    Este modelo se utiliza para representar las categorias del sistema

    Attr
    """
    nombre_categoria = models.CharField(max_length=30, unique=True, blank=False)
    descripcion = models.TextField(max_length=100, blank=False)
    descripcion_corta = models.CharField(max_length=10, blank=False)
    estado = models.BooleanField(default=True)
    moderada = models.BooleanField(default=False)
    tipo_categoria = models.CharField(
        max_length=3,
        choices=TIPO_CATEGORIA_OPCIONES,
        default='PU')
    precio = models.IntegerField(
        null=True
    )
    
    class Meta:
        default_permissions = ()


    def __str__(self):
        return self.nombre_categoria

    def save(self, *args, **kwargs):
        """
        Sobreescribe el método save para convertir descripcion_corta a mayúsculas antes de guardar.
        """
        self.descripcion_corta = self.descripcion_corta.upper()  # Ejemplo: convertir a mayúsculas
        super().save(*args, **kwargs)