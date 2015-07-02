# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_remove_instructor_no_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='no_update',
            field=models.BooleanField(default=False),
        ),
    ]
