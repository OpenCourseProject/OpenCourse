# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_auto_20150629_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='email_address',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
