# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0004_auto_20150629_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('days', models.CharField(max_length=50, db_index=True)),
                ('course_start_time', models.TimeField(db_index=True)),
                ('course_end_time', models.TimeField(db_index=True)),
                ('exam_date', models.DateField()),
                ('exam_start_time', models.TimeField()),
                ('exam_end_time', models.TimeField()),
                ('term', models.ForeignKey(to='course.Term')),
            ],
            options={
                'verbose_name': 'exam period',
                'verbose_name_plural': 'exam periods',
            },
        ),
        migrations.CreateModel(
            name='ExamSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cnu_source', models.URLField()),
                ('xl_source', models.URLField()),
                ('term', models.ForeignKey(to='course.Term')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_crn', models.IntegerField()),
                ('identifier', models.CharField(max_length=100)),
                ('term', models.ForeignKey(to='course.Term')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'scheduled course',
                'verbose_name_plural': 'scheduled courses',
            },
        ),
    ]
