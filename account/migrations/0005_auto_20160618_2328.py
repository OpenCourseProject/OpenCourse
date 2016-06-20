# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20160618_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='default_term',
            field=models.ForeignKey(blank=True, to='course.Term', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='facebook_id',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='learning_community',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='major',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='preferred_name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
