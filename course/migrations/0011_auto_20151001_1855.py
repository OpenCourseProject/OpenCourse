# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_auto_20150821_1746'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='term',
            options={'ordering': ['-value']},
        ),
    ]
