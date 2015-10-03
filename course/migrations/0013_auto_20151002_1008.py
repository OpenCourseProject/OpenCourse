# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_auto_20151002_1007'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='term',
            options={'ordering': ['-priority', '-value']},
        ),
        migrations.RenameField(
            model_name='term',
            old_name='order',
            new_name='priority',
        ),
    ]
