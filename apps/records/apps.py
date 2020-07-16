from django.apps import AppConfig


class RecordsConfig(AppConfig):
    name = "apps.records"

    def ready(self):
        import apps.records.signals
