from django.apps import AppConfig

class CourseConfig(AppConfig):
    name = 'course'
    verbose_name = 'Courses'

    def ready(self):
        import course.signals.handlers
