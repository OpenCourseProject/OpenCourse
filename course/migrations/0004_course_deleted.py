# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_remove_instructor_rmp_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
