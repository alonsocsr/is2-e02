from django.db import models
from categories.models import Categorias
from django.utils import timezone
from datetime import date
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.db.models.signals import pre_save
from django.dispatch import receiver

class Contenido(models.Model):
    
    """
    Modelo para almacenar el contenido creado por los usuarios.

    :cvar titulo: str - Título del contenido.
    :cvar resumen: str - Resumen del contenido.
    :cvar imagen: ImageField - Imagen asociada al contenido.
    :cvar cuerpo: RichTextUploadingField - Cuerpo del contenido en formato enriquecido.
    :cvar autor: User - Usuario que crea el contenido.
    :cvar categoria: Categorias - Categoría a la que pertenece el contenido.
    :cvar fecha_creacion: DateTimeField - Fecha y hora de creación del contenido.
    :cvar fecha_publicacion: DateField - Fecha de publicación del contenido.
    :cvar vigencia: DateField - Fecha de vigencia del contenido.
    :cvar estado: str - Estado del contenido Estado del contenido ('Borrador', 'Edición', 'Publicación', 'Inactivo').
    :cvar activo: bool - Indica si el contenido está activo o no.
    :cvar mensaje_rechazo: str - Mensaje de rechazo del contenido.
    :cvar slug: SlugField - Slug único para el contenido.
    :cvar cantidad_likes: int - Número de "likes" del contenido.
    :cvar cantidad_dislikes: int - Número de "dislikes" del contenido.
    :cvar puntuacion: DecimalField - Puntuación promedio del contenido.
    :cvar cantidad_valoraciones: int - Número total de valoraciones del contenido.
    :cvar cantidad_compartidos: int - Número total de compartidos del contenido.
    :cvar cantidad_vistas: int - Número total de vistas del contenido.
    :cvar fecha_modificacion: DateTimeField - Fecha de la última modificación del contenido.
    :cvar usuario_editor: User - Usuario que editó el contenido.
    :cvar cambios: GenericRelation - Registros de cambios del contenido.
    """
    titulo = models.CharField(max_length=200, default="")
    resumen = models.TextField(default="")
    imagen = models.ImageField(upload_to="content", default=None, null=True)
    cuerpo = RichTextUploadingField(
        default="""
        <p><span style="font-family:Times New Roman,Times,serif"><span style="font-size:20px">Cuerpo del contenido</span></span></p>

        <p><span style="font-family:Times New Roman,Times,serif"><span style="font-size:20px">opcional:image</span></span></p>

        <p><span style="font-family:Times New Roman,Times,serif"><span style="font-size:20px">opcional:embedido youtube</span></span></p>

        <p><span style="font-family:Times New Roman,Times,serif"><span style="font-size:18px"><strong>Tags: <span style="color:#3498db">#Tag1 #Tag2 #Tag3</span></strong></span></span></p>
        """, 
        blank=True, 
        null=True
    )
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    categoria = models.ForeignKey(Categorias, on_delete=models.SET_DEFAULT, default=1)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_publicacion = models.DateField(default=date.today, null=True)
    vigencia = models.DateField(default=None,  null=True)
    estado = models.CharField(max_length=30, default="Borrador")
    activo = models.BooleanField(default=False)
    mensaje_rechazo = models.TextField(blank=True,default="")
    slug = models.SlugField(unique=True, db_index=True, max_length=255)
    # Campos para interaccion
    cantidad_likes = models.PositiveIntegerField(default=0)
    cantidad_dislikes = models.PositiveIntegerField(default=0)
    puntuacion = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    cantidad_valoraciones = models.PositiveIntegerField(default=0)
    cantidad_compartidos = models.PositiveIntegerField(default=0)
    cantidad_vistas = models.PositiveIntegerField(default=0)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_editor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contenidos_editados'
    )

    def save_version(self, user):
        """
        Crea una nueva versión del contenido con los datos actuales.

        :param user: User - Usuario que edita el contenido.
        """
        Version.objects.create(
            contenido=self,
            titulo=self.titulo,
            resumen=self.resumen,
            cuerpo=self.cuerpo,
            fecha_publicacion= self.fecha_publicacion,
            vigencia=self.vigencia,
            fecha_version=timezone.now(),
            editor=user,
        )

    class Meta:
        verbose_name = "Contenido"
        verbose_name_plural = "Contenidos"
        db_table = "contenido"


#clase para almacerar las versiones del contenido borrador y edicion
class Version(models.Model):
    """
    Modelo para almacenar las versiones de un contenido.

    :cvar contenido: ForeignKey - El contenido al que pertenece esta versión.
    :cvar titulo: CharField - Título de la versión.
    :cvar resumen: TextField - Resumen de la versión.
    :cvar cuerpo: RichTextUploadingField - Cuerpo de la versión.
    :cvar fecha_publicacion: DateField - Fecha de publicación de la versión.
    :cvar vigencia: DateField - Fecha de vigencia de la versión.
    :cvar fecha_version: DateTimeField - Fecha y hora de creación de la versión.
    :cvar editor: ForeignKey - Usuario que editó la versión.
    """
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='versiones')
    titulo = models.CharField(max_length=200)
    resumen = models.TextField()
    cuerpo = RichTextUploadingField()
    fecha_publicacion = models.DateField(default=date.today, null=True)
    vigencia = models.DateField(default=None, null=True)
    fecha_version = models.DateTimeField(default=timezone.now)
    editor = models.ForeignKey(
        User,on_delete=models.SET_NULL,
        null=True,
        blank=True,)

    class Meta:
        ordering = ['-fecha_version']
        


class Valoracion(models.Model):
    """
    Modelo que representa una valoración de contenido.

    :cvar contenido: ForeignKey - El contenido que se valora.
    :cvar usuario: ForeignKey - El usuario que realiza la valoración.
    :cvar puntuacion: PositiveIntegerField - Puntuación otorgada (generalmente de 1 a 5).
    :cvar fecha: DateTimeField - Fecha y hora en que se creó la valoración.
    """

    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    puntuacion = models.PositiveIntegerField() 
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Devuelve una representación legible de la valoración.
        :return: Cadena con el formato "Valoración de [nombre de usuario] para [título del contenido]".
        """
        return f"Valoración de {self.usuario.username} para {self.contenido.titulo}"
    

class ContenidoSeleccionado(models.Model):
    """
    Modelo que representa un contenido seleccionado por un usuario.

    :cvar contenido: ForeignKey - El contenido seleccionado.
    :cvar usuario: ForeignKey - El usuario que seleccionó el contenido.
    :cvar fecha: DateTimeField - Fecha y hora en que se seleccionó el contenido.
    """
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-fecha']

REPORTE_OPCIONES = [
    ('odio', 'Mensaje de Odio'),
    ('acoso', 'Acoso'),
    ('privacidad', 'Privacidad'),
    ('difamacion', 'Difamación'),
    ('spam', 'Spam'),
]
class ContenidoReportado(models.Model):
    """
    Modelo para gestionar los reportes de contenido.

    :cvar contenido: ForeignKey - El contenido que se reporta.
    :cvar usuario: ForeignKey - El usuario que realiza el reporte.
    :cvar email: EmailField - El correo electrónico del usuario que reporta.
    :cvar motivo: CharField - Motivo del reporte, basado en las opciones definidas en `REPORTE_OPCIONES`.
    :cvar fecha: DateTimeField - Fecha y hora en que se realizó el reporte.
    """
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(null=True,default=None)
    motivo = models.CharField(
        max_length=50,
        choices=REPORTE_OPCIONES,
        default='spam',
        )
    fecha = models.DateTimeField(auto_now_add=True)

class StatusChangeLog(models.Model):
    """
    Modelo para registrar un historial de cambio del estado del contenido.

    :cvar contenido: ForeignKey - El contenido que se modifica.
    :cvar anterior_estado: CharField - Estado anterior en el que se encontraba el contenido.
    :cvar nuevo_estado: CharField - Nuevo estado al que pasa el contenido.
    :cvar fecha: DateTimeField - Fecha y hora en que se realiza la modificación.
    :cvar modificado_por: ForeignKey - El usuario que realiza la modificación.
    """
    contenido = models.ForeignKey(Contenido, on_delete=models.SET_NULL, null=True)
    anterior_estado = models.CharField(max_length=10)
    nuevo_estado = models.CharField(max_length=10)
    fecha = models.DateTimeField(auto_now=True)
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


@receiver(pre_save, sender=Contenido)
def track_status_change(sender, instance, **kwargs):
    """
    Signal que guarda el estado del contenido antes de que se actualice para uso posterior en la vista donde se crea la historia.

    :param sender: type - El modelo que envía la señal (Contenido).
    :param instance: Contenido - La instancia del modelo que se está guardando.
    :param \**kwargs: dict - Parámetros adicionales pasados a la señal.

    """
    if instance.pk:
        previous_instance = Contenido.objects.get(pk=instance.pk)
        instance._estado_anterior = previous_instance.estado