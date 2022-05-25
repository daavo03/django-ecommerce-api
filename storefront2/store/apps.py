from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    # The code for the signal it's not executed unless we import it. So we overwrite the ready() method this method is 
    #called when this app is ready is initialized
    def ready(self) -> None:
        import store.signals
