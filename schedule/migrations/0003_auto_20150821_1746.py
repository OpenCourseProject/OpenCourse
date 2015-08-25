# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_scheduletransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduletransaction',
            name='action',
            field=models.IntegerField(max_length=4, choices=[(1, b'ADD'), (0, b'Drop')]),
        ),
    ]
