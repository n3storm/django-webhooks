import re
from datetime import datetime

from django.utils import timezone
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

from uuidfield import UUIDField

from .settings import WEB_HOOK_ACTIONS, WEB_HOOK_OWNER_LOCAL, OWNER_MODEL

from .signals import webhook_triggered_signal


class WebHook(models.Model):

    ACTIONS = WEB_HOOK_ACTIONS

    TRIGGER_METHOD = (
        ('G', 'GET'),
        ('H', 'HEAD'),
        ('P', 'POST')
    )

    id = UUIDField(auto=True, primary_key=True)
    owner = models.ForeignKey(OWNER_MODEL, editable=False)  # Editable?
    action = models.CharField(max_length=1, choices=ACTIONS, default='R')
    triggered = models.DateTimeField("Time Triggered", blank=True, null=True)
    method = models.CharField(max_length=1, choices=TRIGGER_METHOD, default='P')
    auth = models.CharField("API Key", max_length=64, blank=True)  # Not used for G / H requests
    filter = models.CharField("Regex Filter Payload", max_length=64, blank=True,
                              help_text='Filter which events apply')  # Not used for HEAD

    # Following fields are required for using GenericForeignKey
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=32)  # Char to support UUID
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField("Date Created", auto_now_add=True)
    updated = models.DateTimeField("Date Updated", auto_now=True)

    class Meta:
        ordering = ['action']

    def __unicode__(self):
        return "%s - %s (%s)" % (self.get_action_display(), self.content_type, self.content_object)

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
        webhook_triggered_signal.send(
            sender=self.__class__,
            triggered=True,
            action=self.action,
            content_object=self.content_object,
            content_type=self.content_type)
          # Update 'triggered' timestamp field
        if settings.USE_TZ:
            self.triggered = datetime.now(tz=timezone.utc)
        else:
            self.triggered = datetime.now()
        self.save()


class Log(models.Model):

    # REQUEST_CONTENT_TYPES = (
    #     ('J', 'application/json'),
    #     ('F', 'application/x-www-form-urlencoded'),
    # )

    HTTP_METHOD = (
        ('G', 'GET'),
        ('H', 'HEAD'),
        ('P', 'POST')
    )

    webhook = models.ForeignKey(WebHook, related_name='logs')
    method = models.CharField(max_length=1, choices=HTTP_METHOD)
    request_content_type = models.CharField(max_length=64)
    payload = models.TextField()
    created = models.DateTimeField("Date Created", auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return "Log of %s - %s (%s)" % (self.webhook.get_action_display(), self.webhook.content_type, self.webhook.content_object)