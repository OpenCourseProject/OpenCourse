# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime

# This migration updates course-related items to indicate when they were created.

class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='followentry',
            name='time_created',
            field=models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instructor',
            name='time_created',
            field=models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='material',
            name='time_created',
            field=models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='term',
            name='time_created',
            field=models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='term',
            name='update',
            field=models.BooleanField(default=True),
        ),
    ]
