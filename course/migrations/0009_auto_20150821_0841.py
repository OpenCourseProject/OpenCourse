# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_auto_20150807_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_crn', models.IntegerField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('data', models.TextField()),
                ('term', models.ForeignKey(to='course.Term')),
            ],
        ),
        migrations.AlterField(
            model_name='course',
            name='meeting_times',
            field=models.ManyToManyField(to='course.MeetingTime', verbose_name=b'Meeting Time', blank=True),
        ),
    ]
