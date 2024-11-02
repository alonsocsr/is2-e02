from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField
from categories.models import Categorias
from content.models import Contenido


class Profile(models.Model):
    """
    La clase Profile define el modelo para el perfil de cada usuario.

    El modelo `Profile` está vinculado uno a uno con el modelo `User` de Django, 
    lo que permite almacenar información adicional sobre el usuario como una imagen de perfil

    :cvar user(OneToOneField): Campo de relación uno a uno con el modelo `User`, que asocia un perfil con un usuario específico.
    :cvar image(ImageField): Campo de imagen que almacena la foto de perfil del usuario. Las imágenes se suben al directorio 'profiles'.
    :cvar categorias_interes(ManyToManyField): Campo de relación de muchos a muchos con el modelo `Categorias`, que almacena las categorías de interés del usuario. Es opcional.
    :cvar suscripciones(ManyToManyField): Campo de relación de muchos a muchos con el modelo `Categorias`, que almacena las categorías a las que el usuario está suscrito. Es opcional.
    :cvar contenidos_like(ManyToManyField): Campo de relación de muchos a muchos con el modelo `Contenido`, que almacena los contenidos a los que el usuario ha dado "like". Es opcional.
    :cvar contenidos_dislike(ManyToManyField): Campo de relación de muchos a muchos con el modelo `Contenido`, que almacena los contenidos a los que el usuario ha dado "dislike". Es opcional.

    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    image = ImageField(upload_to='profiles')
    categorias_interes = models.ManyToManyField(Categorias, blank=True, related_name='categorias_interes')
    contenidos_like = models.ManyToManyField(Contenido, blank=True, related_name='contenidos_like')
    contenidos_dislike = models.ManyToManyField(Contenido, blank=True, related_name='contenidos_dislike')
    class Meta:
        default_permissions = ()

PAYMENT_METHODS = [
        ('TC', 'Tarjeta de Crédito'),
        ('TD', 'Tarjeta de Débito'),
        ('PP', 'PayPal'),
        ('TR', 'Transferencia Bancaria'),
    ]
class Suscripcion(models.Model):
    """
    Modelo Suscripcion que almacena la relación entre un perfil de usuario y una categoría, 
    además de la fecha en que se realiza el pago de la suscripción.

    :cvar profile(ForeignKey): Relación con el modelo Profile que representa al usuario.
    :cvar categoria(ForeignKey): Relación con el modelo Categorias.
    :cvar fecha_pago(DateTimeField): Fecha en la que se realiza el pago de la suscripción.
    """
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='suscripciones')
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.IntegerField(null=True)
    medio_pago = models.CharField(max_length=2, choices=PAYMENT_METHODS)

    class Meta:
        unique_together = ('profile', 'categoria')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    """
    Señal que se ejecuta después de que se guarda un usuario.

    Esta función se encarga de crear un perfil para cada nuevo usuario. Asigna automáticamente 
    el grupo "Admin" al primer usuario y el grupo "Suscriptor" a todos los otros usuarios.

    :param sender: El modelo que envía la señal (User).
    :param instance: La instancia del usuario que se está guardando.
    :param created: Indica si se ha creado un nuevo usuario (bool).
    :param kwargs: Argumentos adicionales pasados a la función.
    """
    if created:
        Profile.objects.create(user=instance)

    if instance.id == 1:
        group = Group.objects.get(name='Admin')
        instance.groups.add(group)
    else:
        group = Group.objects.get(name='Suscriptor')
        instance.groups.add(group)
    
    instance.profile.save()
