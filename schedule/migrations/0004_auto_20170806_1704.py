# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_examsource_active'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='scheduleentry',
            unique_together=set([('user', 'term', 'course_crn')]),
        ),
    ]
