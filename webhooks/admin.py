from django.contrib import admin

from .models import WebHook


class WebHookAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'content_type', '__unicode__', )

admin.site.register(WebHook, WebHookAdmin)