from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from categories.models import Categorias
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

class Contenido(models.Model):
    
    """
    Modelo para almacenar el contenido creado por los usuarios.

    Atributos:
        - titulo (str): Título del contenido.
        - imagen (ImageField): Imagen que se relaciona con el tema del contenido
        - cuerpo (RichTextField): Cuerpo del contenido en formato rico.
        - autor (User): Usuario que crea el contenido.
        - categoria (Categoria): Categoría a la que pertenece el contenido.
        - tipo_contenido (TipoContenido): Tipo de contenido.
        - fecha_creacion (datetime): Fecha y hora de creación del contenido.
        - puntuacion (Decimal): Puntuación promedio del contenido.
        - numero_valoraciones (int): Número total de valoraciones del contenido.
        - estado (str): Estado del contenido. Puede ser 'Borrador', 'Edicion', 'Publicacion' o 'Inactivo'.

    Métodos:
        - for_user(user): Devuelve los contenidos creados por un usuario específico.
        - for_categorias(categorias): Devuelve los contenidos asociados a una lista de categorías.
    """
    titulo = models.CharField(max_length=200, default="titulo")
    imagen = models.ImageField(upload_to="posts", null=True)
    cuerpo = RichTextField(default="cuerpo", blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    categoria = models.ForeignKey(Categorias, on_delete=models.SET_DEFAULT, default=1)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, db_index=True)
    # Campos para interaccion
    puntuacion = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    numero_valoraciones = models.PositiveIntegerField(default=0)
    numero_vistas = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=30, default="Borrador")
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_editor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contenidos_editados'
    )

    cambios = GenericRelation(LogEntry)
    def __str__(self):
        return f"{self.titulo} - {self.autor.first_name} {self.autor.last_name}"

    class Meta:
        verbose_name = "Contenido"
        verbose_name_plural = "Contenidos"
        db_table = "contenido"


#signal para cargar el slug
@receiver(pre_save, sender=Contenido)
def update_slug(sender, instance, **kwargs):
    if instance.titulo:
        instance.slug = slugify(instance.titulo)

class Valoracion(models.Model):
    """
    Modelo que representa una valoración de contenido.

    Atributos:
        contenido (Contenido): El contenido que se valora.
        usuario (User): El usuario que realiza la valoración.
        puntuacion (int): La puntuación otorgada, generalmente en un rango de 1 a 5.
        fecha (datetime): La fecha y hora en que se creó la valoración.

    Métodos:
        __str__(): Devuelve una representación legible de la valoración.

    Atributos:
        contenido (Contenido): El contenido que se valora.
        usuario (User): El usuario que realiza la valoración.
        puntuacion (int): La puntuación otorgada, generalmente en un rango de 1 a 5.
        fecha (datetime): La fecha y hora en que se creó la valoración.
    """

    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    puntuacion = models.PositiveIntegerField()  # Aquí puedes usar un rango de 1 a 5, por ejemplo
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Devuelve una representación legible de la valoración.
        :return: Cadena con el formato "Valoración de [nombre de usuario] para [título del contenido]".
        """
        return f"Valoración de {self.usuario.username} para {self.contenido.titulo}"