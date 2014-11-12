# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks', '0002_auto_20141106_1323'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='log',
            options={'ordering': ['created']},
        ),
        migrations.AlterField(
            model_name='log',
            name='webhook',
            field=models.ForeignKey(related_name='logs', to='webhooks.WebHook'),
            preserve_default=True,
        )
    ]
