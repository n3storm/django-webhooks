try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse

from django.views.generic.edit import UpdateView
from django.views.decorators.csrf import csrf_exempt

from .models import WebHook


class WebHookView(UpdateView):

    http_method_names = [u'get', u'post', u'head']
    model = WebHook
    template_name = 'webhook/action.html'

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
        return super(WebHookView, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # TODO: Check obj.auth
        obj = self.get_object()
        if obj.get_method_display() == request.method and obj.filter is not None:
            ct = request.META.get('CONTENT_TYPE', None)
            if ct == 'application/x-www-form-urlencoded':
                payload = str(urlparse.parse_qs(request.body))
            else:
                payload = str(request.body)
            if obj.match_filter(payload):
                obj.trigger()
        return super(WebHookView, self).post(request, *args, **kwargs)
