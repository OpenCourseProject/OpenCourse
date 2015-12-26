from django.apps import AppConfig

class OpenCourseConfig(AppConfig):
    name = 'opencourse'
    verbose_name = 'OpenCourse'

    def ready(self):
        import opencourse.signals.handlers
