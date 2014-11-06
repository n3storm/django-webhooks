# DNS Manager for Django

Reusable Django app that allows for webhooks to be consumed.

Emits a signal `webhook_triggered_signal` when the webhook is triggered. This allows you to provide an action for the
webhook.

This is used by [Volt Grid](https://www.voltgrid.com/).

[![Build Status](https://travis-ci.org/voltgrid/django-webhooks.svg?branch=master)](https://travis-ci.org/voltgrid/django-webhooks)
[![Coverage Status](https://coveralls.io/repos/voltgrid/django-webhooks/badge.png)](https://coveralls.io/r/voltgrid/django-webhooks)

## Installation

Install with pip:

	pip install git+https://github.com/voltgrid/django-webhooks.git#egg=webhooks

Add to your Django project in your Python path.

Add `webhooks` to your `INSTALLED_APPS`.

Set `WEB_HOOK_USER` in `settings.py`. This must point to a model that provides a _user_ field. Eg:

    class User(models.Model):
    
        user = models.ForeignKey(User)
        name = models.CharField(max_length=64)
    
        class Meta:
            ordering = ['name']
    
        def __unicode__(self):
            return "%s" % self.name
            
Run `manage.py syncdb`.

## Testing

1. Checkout the source.
2. Install all the requirements `pip install -r requirements.txt.`
3. Then run `./manage.py test`.

### Triggering with curl

    curl -H "Content-Type: application/json" -d "${DATA}" ${URL}

Where `$DATA` is JSON payload that will pass the regex, and `$URL` is the webhook URL.
