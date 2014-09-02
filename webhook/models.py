import re
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django.db import models
import django.dispatch
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy

from uuidfield import UUIDField

from default_settings import WEB_HOOK_OWNER_MODEL, WEB_HOOK_ACTIONS, WEB_HOOK_OWNER_LOCAL

# Load defaults
if hasattr(settings, 'WEB_HOOK_OWNER_MODEL'):
    WEB_HOOK_OWNER_MODEL = settings.WEB_HOOK_OWNER_MODEL

if hasattr(settings, 'WEB_HOOK_ACTIONS'):
    WEB_HOOK_ACTIONS = settings.WEB_HOOK_ACTIONS

# Work out our dynamic relation
app_name = WEB_HOOK_OWNER_MODEL.rsplit('.', 1)[0]
model_name = WEB_HOOK_OWNER_MODEL.rsplit('.', 1)[1]
module = __import__(app_name, fromlist=[model_name])
owner_model = getattr(module, model_name)

# signal
webhook_triggered_signal = django.dispatch.Signal(providing_args=['action', 'content_object'])


class WebHook(models.Model):

    ACTIONS = WEB_HOOK_ACTIONS

    TRIGGER_METHOD = (
        ('G', 'GET'),
        ('H', 'HEAD'),
        ('P', 'POST')
    )

    id = UUIDField(auto=True, primary_key=True)
    owner = models.ForeignKey(owner_model, editable=False)  # Editable?
    action = models.CharField(max_length=1, choices=ACTIONS, default='R')
    triggered = models.DateTimeField("Time Triggered", auto_now=True)
    method = models.CharField(max_length=1, choices=TRIGGER_METHOD, default='P')
    auth = models.CharField("API Key", max_length=64, blank=True)  # Not used for G / H requests
    filter = models.CharField("Regex Filter Payload", max_length=64, blank=True, help_text='Filter which events apply')  # Not used for HEAD

    # Following fields are required for using GenericForeignKey
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=32)  # Char to support UUID
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField("Date Created", auto_now_add=True)
    updated = models.DateTimeField("Date Updated", auto_now=True)

    class Meta:
        ordering = ['action']

    def __unicode__(self):
        return "%s - %s - %s" % (self.get_action_display(), self.get_method_display(), self.content_type)

    def get_absolute_url(self):
        return reverse_lazy('web-hook', kwargs={'pk': self.pk})

    @property
    def owner_src(self):
        return self.content_object.owner_src  # TODO: Make this configurable

    def clean(self):
        self.validate_regex()
        if not WEB_HOOK_OWNER_LOCAL:
            self.owner = self.owner_src  # update owner before save
        super(self.__class__, self).clean()

    def validate_regex(self):
        try:
            if self.filter is not None:
                re.compile(self.filter)
        except Exception as e:
            raise

    def match_filter(self, data):
        if self.filter is not None:
            if re.search(self.filter, data) is not None:
                return True
            else:
                return False
        else:
            return True

    def trigger(self):
        webhook_triggered_signal.send(sender=self.__class__, action=self.action, content_object=self.content_object)
        self.save()  # Update triggered field