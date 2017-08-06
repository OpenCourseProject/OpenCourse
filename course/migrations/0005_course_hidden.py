# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_course_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
