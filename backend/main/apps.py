from django.apps import AppConfig

from django.db.models.signals import post_save, post_delete, post_migrate

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from . import signals  # выполнение модуля -> регистрация сигналов
        # post_migrate.connect(signals.migrations_made, sender=self)