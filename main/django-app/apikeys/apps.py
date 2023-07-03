from django.apps import AppConfig


class ApikeysConfig(AppConfig):
    """
    AppConfig for the 'apikeys' app.

    This class represents the configuration for the 'apikeys' app.
    It specifies the default auto field and the name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apikeys'
