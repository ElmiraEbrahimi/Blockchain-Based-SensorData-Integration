from django.apps import AppConfig
from django.db import OperationalError


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        try:
            from .models import MiddlewareFilter
            middleware_filter, _ = MiddlewareFilter.objects.get_or_create()
        except OperationalError:
            pass
