from django.apps import AppConfig


class MainAppConfig(AppConfig):
    name = 'MAIN_APP'
    def ready(self):
        from MAIN_APP import signals


