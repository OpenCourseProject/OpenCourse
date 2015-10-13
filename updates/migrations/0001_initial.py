# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('body_markdown', models.TextField()),
                ('body', models.TextField(editable=False)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('scripts', models.TextField(null=True, blank=True)),
                ('styles', models.TextField(null=True, blank=True)),
                ('published', models.BooleanField(default=False)),
            ],
        ),
    ]
