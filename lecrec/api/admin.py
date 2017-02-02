from django.contrib import admin
from api.models import Record


class RecordAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ('id', 'filename', 'user', 'created', )


admin.site.register(Record, RecordAdmin)
