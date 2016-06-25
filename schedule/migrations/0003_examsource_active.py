# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20151223_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='examsource',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
