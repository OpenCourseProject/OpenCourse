# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('learning_community', models.CharField(max_length=100, null=True)),
                ('facebook_id', models.CharField(max_length=50, null=True)),
                ('default_term', models.ForeignKey(to='course.Term', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('preferred_name', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
