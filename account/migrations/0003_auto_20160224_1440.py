# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_show_archived_terms'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='show_colors_schedule',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='show_details_schedule',
            field=models.BooleanField(default=True),
        ),
    ]
