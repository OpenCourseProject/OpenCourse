# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20150821_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduletransaction',
            name='action',
            field=models.IntegerField(choices=[(1, b'ADD'), (0, b'DROP')]),
        ),
    ]
