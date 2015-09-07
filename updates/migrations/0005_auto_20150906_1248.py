# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0004_update_scripts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update',
            name='scripts',
            field=models.TextField(null=True, blank=True),
        ),
    ]
