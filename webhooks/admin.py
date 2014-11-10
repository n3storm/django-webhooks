from django.contrib import admin

from .models import WebHook, Log


class WebHookAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'content_type', '__unicode__', )

class LogAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'created' )

admin.site.register(WebHook, WebHookAdmin)
admin.site.register(Log, LogAdmin)