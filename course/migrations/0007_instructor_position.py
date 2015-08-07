# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_auto_20150806_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='position',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Position', blank=True),
        ),
    ]
