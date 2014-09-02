from django.conf.urls import patterns, include, url

from .views import WebHookView

urlpatterns = patterns('',
    url(r'^web-hook/(?P<pk>[-_\d\w]+)/$', WebHookView.as_view(), name='web-hook'),
)
