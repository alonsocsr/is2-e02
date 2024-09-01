from django.apps import AppConfig


class PermissionsConfig(AppConfig):
    """ Configuración de la aplicación de permisos. 
        Parámetros:
        -----------
        AppConfig : django.apps.AppConfig
            Clase base para la configuración de aplicaciones Django.

        Returns:
        --------
        None
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'permissions'
