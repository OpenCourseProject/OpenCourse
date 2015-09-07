# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0003_auto_20150825_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='scripts',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
