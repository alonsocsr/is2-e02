from django.apps import AppConfig


class ContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'
    # desactivo mientras que no se necesite, descomentar las lineas para mandar al correo
    def ready(self):
            import content.signals