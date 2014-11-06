# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebHook',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, serialize=False, editable=False, max_length=32, blank=True, unique=True)),
                ('action', models.CharField(default=b'R', max_length=1, choices=[(b'S', b'Start'), (b'H', b'Halt'), (b'R', b'Restart')])),
                ('triggered', models.DateTimeField(auto_now=True, verbose_name=b'Time Triggered')),
                ('method', models.CharField(default=b'P', max_length=1, choices=[(b'G', b'GET'), (b'H', b'HEAD'), (b'P', b'POST')])),
                ('auth', models.CharField(max_length=64, verbose_name=b'API Key', blank=True)),
                ('filter', models.CharField(help_text=b'Filter which events apply', max_length=64, verbose_name=b'Regex Filter Payload', blank=True)),
                ('object_id', models.CharField(max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'Date Updated')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('owner', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['action'],
            },
            bases=(models.Model,),
        ),
    ]
