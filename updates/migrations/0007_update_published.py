# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0006_update_styles'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
