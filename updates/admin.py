from django.contrib import admin
from updates.models import Update

@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    exclude = ('body',)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()
