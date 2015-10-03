# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opencourse', '0005_auto_20151001_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='acknowledged',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
