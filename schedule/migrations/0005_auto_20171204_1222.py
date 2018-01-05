# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_auto_20170806_1704'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='examentry',
            unique_together=set([('term', 'days', 'course_start_time', 'course_end_time')]),
        ),
    ]
