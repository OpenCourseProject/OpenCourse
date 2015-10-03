# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opencourse', '0002_report_responded'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('style', models.CharField(max_length=10, choices=[(b'success', b'Success'), (b'info', b'Info'), (b'warning', b'Warning'), (b'danger', b'Danger')])),
                ('message', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]
