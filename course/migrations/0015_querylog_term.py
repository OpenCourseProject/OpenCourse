# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_querylog'),
    ]

    operations = [
        migrations.AddField(
            model_name='querylog',
            name='term',
            field=models.ForeignKey(default=None, to='course.Term'),
            preserve_default=False,
        ),
    ]
