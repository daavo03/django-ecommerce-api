from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    # Loading the signals module from the core when the app is ready
    def ready(self) -> None:
        import core.signals.handlers