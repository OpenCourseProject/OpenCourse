# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opencourse', '0003_auto_20151228_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='termupdate',
            name='courses_deleted',
            field=models.IntegerField(default=0),
        ),
    ]
