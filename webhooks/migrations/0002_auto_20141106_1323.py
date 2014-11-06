# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('method', models.CharField(max_length=1, choices=[(b'G', b'GET'), (b'H', b'HEAD'), (b'P', b'POST')])),
                ('request_content_type', models.CharField(max_length=64)),
                ('payload', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('webhook', models.ForeignKey(to='webhooks.WebHook')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='webhook',
            name='triggered',
            field=models.DateTimeField(null=True, verbose_name=b'Time Triggered', blank=True),
        ),
    ]
