from distutils.version import Version
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from categories.models import Categorias
from django.utils import timezone
from datetime import date
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

class Contenido(models.Model):
    
    """
    Modelo para almacenar el contenido creado por los usuarios.

    Atributos:
        - titulo (str): Título del contenido.
        - cuerpo (RichTextField): Cuerpo del contenido en formato rico.
        - autor (User): Usuario que crea el contenido.
        - categoria (Categoria): Categoría a la que pertenece el contenido.
        - tipo_contenido (TipoContenido): Tipo de contenido.
        - fecha_creacion (datetime): Fecha y hora de creación del contenido.
        - puntuacion (Decimal): Puntuación promedio del contenido.
        - numero_valoraciones (int): Número total de valoraciones del contenido.
        - estado (str): Estado del contenido. Puede ser 'Borrador', 'Edicion', 'Publicacion' o 'Inactivo'.

    Métodos:
        - save_version(self): Crea una versión del contenido cuando cambios son hechos
    """
    titulo = models.CharField(max_length=200, default="titulo")
    resumen = models.TextField(default="resumen")
    imagen = models.ImageField(upload_to="content", default=None, null=True)
    cuerpo = RichTextUploadingField(default="cuerpo", blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    categoria = models.ForeignKey(Categorias, on_delete=models.SET_DEFAULT, default=1)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_publicacion = models.DateField(default=date.today)
    vigencia = models.DateField(default=date.today)
    estado = models.CharField(max_length=30, default="Borrador")
    activo = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, db_index=True)
    # Campos para interaccion
    cantidad_likes = models.PositiveIntegerField(default=0)
    cantidad_dislikes = models.PositiveIntegerField(default=0)
    puntuacion = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    cantidad_valoraciones = models.PositiveIntegerField(default=0)
    cantidad_vistas = models.PositiveIntegerField(default=0)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_editor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contenidos_editados'
    )
    cambios = GenericRelation(LogEntry)

    def save_version(self):
        Version.objects.create(
            contenido=self,
            titulo=self.titulo,
            resumen=self.resumen,
            cuerpo=self.cuerpo,
            fecha_publicacion= self.fecha_publicacion,
            vigencia=self.vigencia,
            fecha_version=timezone.now()
        )


    def __str__(self):
        return f"{self.titulo} - {self.autor.first_name} {self.autor.last_name}"

    class Meta:
        verbose_name = "Contenido"
        verbose_name_plural = "Contenidos"
        db_table = "contenido"


#clase para almacerar las versiones del contenido borrador y edicion
class Version(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='versiones')
    titulo = models.CharField(max_length=200)
    resumen = models.TextField()
    cuerpo = RichTextUploadingField()
    fecha_publicacion = models.DateField(default=date.today)
    vigencia = models.DateField(default=date.today)
    fecha_version = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-fecha_version']
        


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
    puntuacion = models.PositiveIntegerField() 
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Devuelve una representación legible de la valoración.
        :return: Cadena con el formato "Valoración de [nombre de usuario] para [título del contenido]".
        """
        return f"Valoración de {self.usuario.username} para {self.contenido.titulo}"
    
    