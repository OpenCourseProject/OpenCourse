# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0005_auto_20150906_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='styles',
            field=models.TextField(null=True, blank=True),
        ),
    ]
