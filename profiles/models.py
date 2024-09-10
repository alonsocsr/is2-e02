from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField
from categories.models import Categorias


class Profile(models.Model):
    """
    La clase Profile define el modelo para el perfil de cada usuario.

    El modelo `Profile` está vinculado uno a uno con el modelo `User` de Django, 
    lo que permite almacenar información adicional sobre el usuario como una imagen de perfil

    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    image = ImageField(upload_to='profiles')
    categorias_interes = models.ManyToManyField(Categorias, blank=True, related_name='categorias_interes')
    suscripciones = models.ManyToManyField(Categorias, blank=True, related_name='suscripciones')

    class Meta:
        default_permissions = ()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    """
    Señal que se ejecuta después de que se guarda un usuario.

    Esta función se encarga de crear un perfil para cada nuevo usuario. Asigna automáticamente 
    el grupo "Admin" al primer usuario y el grupo "Suscriptor" a todos los otros usuarios.

    Args:
        sender: El modelo que envía la señal (User).
        instance: La instancia del usuario que se está guardando.
        created (bool): Indica si se ha creado un nuevo usuario.
        **kwargs: Argumentos adicionales.
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
