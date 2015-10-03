# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opencourse', '0003_alert'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='message',
            field=models.CharField(max_length=1000),
        ),
    ]
