from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField

"""
La clase Profile define el modelo para el perfil de cada usuario

"""


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    image = ImageField(upload_to='profiles')

    class Meta:
        default_permissions = ()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crea un nuevo perfil cuando un usuario es creado
    """
    if created:
        Profile.objects.create(user=instance)

    if instance.id == 1:
        group = Group.objects.get(name='Admin')
        instance.groups.add(group)
        instance.profile.save()
    else:
        group = Group.objects.get(name='Suscriptor')
        instance.groups.add(group)
        instance.profile.save()
