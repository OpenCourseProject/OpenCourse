# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0017_remove_querylog_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='querylog',
            name='results',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
