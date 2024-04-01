from django.apps import AppConfig


class UserpuzzleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userpuzzle'

    def ready(self):
        # from .background import start
        # start()
        pass
