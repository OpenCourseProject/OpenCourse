# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20160224_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='major',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='orientation',
            field=models.BooleanField(default=False),
        ),
    ]
