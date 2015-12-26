# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime

# This migration updates schedule items to indicate when they were created.

class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleentry',
            name='time_created',
            field=models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scheduletransaction',
            name='time_created',
            field=models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True),
            preserve_default=False,
        ),
    ]
