from django.apps import AppConfig

class AccountConfig(AppConfig):
    name = 'account'
    verbose_name = 'Account'

    def ready(self):
        import account.signals.handlers
