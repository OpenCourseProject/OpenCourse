# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0005_instructor_email_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructorSuggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('email_address', models.EmailField(max_length=254, null=True, blank=True)),
                ('rmp_link', models.URLField(null=True, blank=True)),
                ('instructor', models.ForeignKey(to='course.Instructor')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='instructorlinksuggestion',
            name='instructor',
        ),
        migrations.RemoveField(
            model_name='instructorlinksuggestion',
            name='user',
        ),
        migrations.DeleteModel(
            name='InstructorLinkSuggestion',
        ),
    ]
