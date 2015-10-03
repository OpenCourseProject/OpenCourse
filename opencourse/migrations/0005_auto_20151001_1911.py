# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opencourse', '0004_auto_20151001_1907'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='active',
            new_name='enabled',
        ),
        migrations.AddField(
            model_name='alert',
            name='expires',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
