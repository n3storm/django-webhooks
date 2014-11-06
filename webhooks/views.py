try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse

try:
    from urllib import unquote_plus
except ImportError:
    from urllib.parse import unquote_plus

from django.views.generic.edit import UpdateView
from django.views.decorators.csrf import csrf_exempt

from .models import WebHook, Log
from .settings import WEB_HOOK_LOG_ENABLED


class WebHookView(UpdateView):

    http_method_names = [u'get', u'post', u'head']
    model = WebHook
    template_name = 'webhooks/webhook_detail.html'

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(WebHookView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        # TODO: Check obj.auth
        obj = self.get_object()
        if obj.get_method_display() == request.method and obj.filter is not None:
            payload = str(urlparse.parse_qs(request.path))
            if obj.match_filter(payload):
                obj.trigger()
            if WEB_HOOK_LOG_ENABLED:
                log = Log.objects.create(
                    webhook=obj,
                    method='G',
                    request_content_type=request.META.get('CONTENT_TYPE', ''),
                    payload=payload)
        return super(WebHookView, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # TODO: Check obj.auth
        obj = self.get_object()
        if obj.get_method_display() == request.method and obj.filter is not None:
            ct = request.META.get('CONTENT_TYPE', None)
            if ct == 'application/x-www-form-urlencoded':
                payload = str(unquote_plus(request.body))
                print payload
            else:
                payload = str(request.body)
            if obj.match_filter(payload):
                obj.trigger()
            if WEB_HOOK_LOG_ENABLED:
                log = Log.objects.create(
                    webhook=obj,
                    method='P',
                    request_content_type=request.META.get('CONTENT_TYPE', ''),
                    payload=payload)
        return super(WebHookView, self).post(request, *args, **kwargs)
