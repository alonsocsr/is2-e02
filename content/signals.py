# content/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlencode
from .models import StatusChangeLog

@receiver(post_save, sender=StatusChangeLog)
def enviar_notificacion_cambio_estado(sender, instance, created, **kwargs):
    if created:
        contenido = instance.contenido
        autor = contenido.autor.email if contenido and contenido.autor else None
        usuario_modifico = instance.modificado_por.username if instance.modificado_por else "Alguien"
        
        if autor:
            # Construir URL dinámicamente
            base_url = f"http://localhost/detalle-contenido/{contenido.slug}/"
            query_params = urlencode({'is_staff': 'true'})
            full_url = f"{base_url}?{query_params}"
            
            asunto = f"El estado de tu contenido '{contenido.titulo}' ha cambiado"
            
            mensaje = (
                f"Hola {contenido.autor},\n\n"
                f"El estado de tu contenido '{contenido.titulo}' ha cambiado de '{instance.anterior_estado}' "
                f"a '{instance.nuevo_estado}' por {usuario_modifico}.\n\n"
            )
            
            # Añadir el enlace para revisar el contenido
            mensaje += f"Puedes revisarlo en la plataforma usando el siguiente enlace: {full_url}\n\n"
            mensaje += "Saludos,\nEl equipo de CMS Stark"

            # Enviar correo al autor
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [autor],
                fail_silently=False
            )
