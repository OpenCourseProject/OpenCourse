# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='update',
            name='body',
        ),
        migrations.RemoveField(
            model_name='update',
            name='body_markdown',
        ),
        migrations.RemoveField(
            model_name='update',
            name='scripts',
        ),
        migrations.AddField(
            model_name='update',
            name='identifier',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
