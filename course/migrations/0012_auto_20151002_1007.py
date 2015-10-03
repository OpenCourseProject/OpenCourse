# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_auto_20151001_1855'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='term',
            options={'ordering': ['-order', '-value']},
        ),
        migrations.AddField(
            model_name='term',
            name='order',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
