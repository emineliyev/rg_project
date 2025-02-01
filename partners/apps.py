from django.apps import AppConfig


class PartnersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'partners'
    verbose_name = '6. Tərəfdaşlar'

    def ready(self):
        import partners.signals
