# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

# This migration updates the UpdateLog (CourseUpdateLog) to support process output
# logging as well as completion indication for better monitoring.
# Added: TermUpdate

class Migration(migrations.Migration):

    dependencies = [
        ('opencourse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseupdatelog',
            name='output',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='courseupdatelog',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'In Progress'), (1, b'Success'), (2, b'Failed')]),
        ),
        migrations.AddField(
            model_name='courseupdatelog',
            name='time_completed',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.CreateModel(
            name='TermUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('courses_parsed', models.IntegerField(default=0)),
                ('courses_added', models.IntegerField(default=0)),
                ('courses_updated', models.IntegerField(default=0)),
                ('time_completed', models.DateTimeField(null=True, blank=True)),
                ('term', models.ForeignKey(to='course.Term')),
            ],
        ),
        migrations.RemoveField(
            model_name='courseupdatelog',
            name='courses_added',
        ),
        migrations.RemoveField(
            model_name='courseupdatelog',
            name='courses_parsed',
        ),
        migrations.RemoveField(
            model_name='courseupdatelog',
            name='courses_updated',
        ),
        migrations.AddField(
            model_name='courseupdatelog',
            name='updates',
            field=models.ManyToManyField(to='opencourse.TermUpdate'),
        ),
    ]
