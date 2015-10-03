# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0016_querylog_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='querylog',
            name='result',
        ),
    ]
