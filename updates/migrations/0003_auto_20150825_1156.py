# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0002_auto_20150825_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update',
            name='time_created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
