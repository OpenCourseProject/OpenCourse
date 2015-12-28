# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opencourse', '0002_courseupdatelog_output'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CourseUpdateLog',
            new_name='UpdateLog',
        ),
    ]
