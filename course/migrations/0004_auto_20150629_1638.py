# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_instructor_no_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='rmp_link',
            field=models.URLField(max_length=100, null=True, verbose_name=b'RateMyProfessor Link', blank=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='rmp_score',
            field=models.DecimalField(null=True, verbose_name=b'Rating', max_digits=2, decimal_places=1, blank=True),
        ),
    ]
