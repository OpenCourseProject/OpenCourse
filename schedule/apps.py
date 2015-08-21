from django.apps import AppConfig

class ScheduleConfig(AppConfig):
    name = 'schedule'
    verbose_name = 'Schedule'

    def ready(self):
        import schedule.signals.handlers
