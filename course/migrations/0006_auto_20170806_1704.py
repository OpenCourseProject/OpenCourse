# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_course_hidden'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='followentry',
            unique_together=set([('user', 'term', 'course_crn')]),
        ),
    ]
