# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20151223_2335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructor',
            name='rmp_score',
        ),
    ]
