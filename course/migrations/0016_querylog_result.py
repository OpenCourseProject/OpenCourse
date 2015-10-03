# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_querylog_term'),
    ]

    operations = [
        migrations.AddField(
            model_name='querylog',
            name='result',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
