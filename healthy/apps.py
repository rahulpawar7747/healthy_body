from django.apps import AppConfig

class HealthyConfig(AppConfig):
    name = 'healthy'

    def ready(self):
        from .scheduler import start
        start()