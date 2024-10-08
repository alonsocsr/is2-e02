from django.db import models

TIPO_CATEGORIA_OPCIONES = [
    ('PU', 'Pública'),
    ('GR', 'Gratuita'),
    ('PA', 'Paga'),
]

class Categorias(models.Model):
    """
    Modelo que representa una categoría en el sistema.

    :cvar nombre_categoria(CharField): El nombre de la categoría, debe ser único y no puede estar en blanco.
    :cvar descripcion(TextField): Una descripción detallada de la categoría.
    :cvar descripcion_corta(CharField): Una descripción corta de la categoría.
    :cvar estado(BooleanField): Estado de la categoría, por defecto es ``True``.
    :cvar moderada(BooleanField): Indica si la categoría está moderada, por defecto es ``True``.
    :cvar prioridad(BooleanField): Indica si la categoría tiene prioridad de visualización sobre otras categorías. Puede haber hasta 5 categorías con prioridad activa.
    :cvar tipo_categoria(CharField): Tipo de la categoría, elige entre las opciones definidas en `TIPO_CATEGORIA_OPCIONES`, por defecto es 'PU'.
    :cvar precio(IntegerField): Precio asociado a la categoría, puede ser `None`.
    """
    nombre_categoria = models.CharField(max_length=30, unique=True, blank=False)
    descripcion = models.TextField(max_length=100, blank=False)
    descripcion_corta = models.CharField(max_length=10, blank=False)
    estado = models.BooleanField(default=True)
    moderada = models.BooleanField(default=True)  # Valor por defecto
    prioridad = models.BooleanField(default=False)
    tipo_categoria = models.CharField(
        max_length=3,
        choices=TIPO_CATEGORIA_OPCIONES,
        default='PU',
        )
    precio = models.IntegerField(null=True)


    class Meta:
        default_permissions = ()

    def __str__(self):
        """
        Retorna una representación en cadena de la categoría.

        :return: str: El nombre de la categoría.
        """
        return self.nombre_categoria

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método de guardado para ajustar el precio y convertir la descripción corta a mayúsculas.

        Asigna un precio fijo de 20000 si el tipo de categoría es 'PA', es decir, de Pago. De lo contrario, el precio se establece en `None`.
        La descripción corta se convierte a mayúsculas antes de guardar.

        :param args: Argumentos adicionales pasados al método `save` del modelo.
        :param kwargs: Palabras clave adicionales pasadas al método `save` del modelo.
        """
        
        if self.tipo_categoria == 'PA':
            self.precio = 20000
        else:
            self.precio = None 

        self.descripcion_corta = self.descripcion_corta.upper()
        
        super().save(*args, **kwargs)
