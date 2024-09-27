# content/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import StatusChangeLog

@receiver(post_save, sender=StatusChangeLog)
def enviar_notificacion_cambio_estado(sender, instance, created, **kwargs):
    if created:
        # Obtenemos el contenido, autor y otros detalles para el correo
        contenido = instance.contenido
        autor = contenido.autor.email if contenido and contenido.autor else None
        usuario_modifico = instance.modificado_por.username if instance.modificado_por else "Alguien"

        if autor:
            asunto = f"El estado de tu contenido '{contenido.titulo}' ha cambiado"
            mensaje = (
                f"Hola {contenido.autor},\n\n"
                f"El estado de tu contenido '{contenido.titulo}' ha cambiado de '{instance.anterior_estado}' "
                f"a '{instance.nuevo_estado}' por {usuario_modifico}.\n\n"
                "Puedes revisarlo en la plataforma.\n\n"
                "Saludos,\nEl equipo de CMS Stark"
            )
            # Enviar correo al autor
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [autor],
                fail_silently=False
            )
