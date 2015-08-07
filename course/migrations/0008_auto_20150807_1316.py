# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_instructor_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='attributes',
            field=models.CharField(max_length=10, null=True, verbose_name=b'Attributes', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(verbose_name=b'Instructor', blank=True, to='course.Instructor', null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='location',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Location', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='meeting_times',
            field=models.ManyToManyField(to='course.MeetingTime', blank=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='email_address',
            field=models.EmailField(default=None, max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='position',
            field=models.CharField(default=None, max_length=100, null=True, verbose_name=b'Position', blank=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='rmp_link',
            field=models.URLField(default=None, max_length=100, null=True, verbose_name=b'RateMyProfessor Link', blank=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='rmp_score',
            field=models.DecimalField(decimal_places=1, default=None, max_digits=2, blank=True, null=True, verbose_name=b'Rating'),
        ),
    ]
