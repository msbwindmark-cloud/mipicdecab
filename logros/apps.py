from django.apps import AppConfig


class LogrosConfig(AppConfig):
    name = 'logros'

    def ready(self):
        from . import signals  # noqa
