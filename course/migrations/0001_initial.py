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
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=10, verbose_name=b'Attribute Value')),
                ('name', models.CharField(max_length=50, verbose_name=b'Attribute Name')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('crn', models.IntegerField(verbose_name=b'CRN', db_index=True)),
                ('course', models.CharField(max_length=50, verbose_name=b'Course', db_index=True)),
                ('course_link', models.URLField(verbose_name=b'Course Link')),
                ('section', models.CharField(max_length=5, verbose_name=b'Section')),
                ('title', models.CharField(max_length=50, verbose_name=b'Title')),
                ('bookstore_link', models.URLField(verbose_name=b'Bookstore Link')),
                ('hours', models.CharField(max_length=5, verbose_name=b'Hours')),
                ('attributes', models.CharField(max_length=10, verbose_name=b'Attributes')),
                ('ctype', models.CharField(max_length=10, verbose_name=b'Type')),
                ('location', models.CharField(max_length=20, null=True, verbose_name=b'Location')),
                ('seats', models.IntegerField(verbose_name=b'Seats Left', db_index=True)),
                ('status', models.IntegerField(verbose_name=b'Status')),
            ],
            options={
                'verbose_name': 'course',
                'verbose_name_plural': 'courses',
            },
        ),
        migrations.CreateModel(
            name='FollowEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_crn', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50, null=True, verbose_name=b'First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name=b'Last Name', db_index=True)),
                ('rmp_score', models.DecimalField(null=True, verbose_name=b'Rating', max_digits=2, decimal_places=1, blank=True)),
                ('rmp_link', models.URLField(max_length=100, null=True, verbose_name=b'RateMyProfessor Link', blank=True)),
                ('no_update', models.BooleanField(default=False)),
                ('email_address', models.EmailField(max_length=254, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_crn', models.IntegerField()),
                ('isbn', models.BigIntegerField(null=True)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=50)),
                ('publisher', models.CharField(max_length=50)),
                ('edition', models.CharField(max_length=20)),
                ('year', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MeetingTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('days', models.CharField(max_length=50, verbose_name=b'Days', db_index=True)),
                ('start_time', models.TimeField(null=True, verbose_name=b'Start', db_index=True)),
                ('end_time', models.TimeField(null=True, verbose_name=b'End', db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('value', models.IntegerField(unique=True, serialize=False, verbose_name=b'Term Value', primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Term Name')),
            ],
        ),
        migrations.AddField(
            model_name='material',
            name='term',
            field=models.ForeignKey(to='course.Term'),
        ),
        migrations.AddField(
            model_name='followentry',
            name='term',
            field=models.ForeignKey(to='course.Term'),
        ),
        migrations.AddField(
            model_name='followentry',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(verbose_name=b'Instructor', blank=True, to='course.Instructor', null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='meeting_times',
            field=models.ManyToManyField(to=b'course.MeetingTime', verbose_name=b'Meeting Time', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='term',
            field=models.ForeignKey(to='course.Term'),
        ),
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
        migrations.AddField(
            model_name='instructor',
            name='position',
            field=models.CharField(default=None, max_length=100, null=True, verbose_name=b'Position', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='attributes',
            field=models.CharField(max_length=10, null=True, verbose_name=b'Attributes', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='location',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Location', blank=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='email_address',
            field=models.EmailField(default=None, max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='rmp_link',
            field=models.URLField(default=None, max_length=100, null=True, verbose_name=b'RateMyProfessor Link', blank=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='rmp_score',
            field=models.DecimalField(decimal_places=1, default=None, max_digits=2, blank=True, null=True, verbose_name=b'Rating'),
        ),
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
            name='status',
            field=models.IntegerField(verbose_name=b'Status', choices=[(1, b'Open'), (0, b'Closed')]),
        ),
        migrations.AlterModelOptions(
            name='term',
            options={'ordering': ['-value']},
        ),
        migrations.AlterModelOptions(
            name='term',
            options={'ordering': ['-order', '-value']},
        ),
        migrations.AddField(
            model_name='term',
            name='order',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterModelOptions(
            name='term',
            options={'ordering': ['-priority', '-value']},
        ),
        migrations.RenameField(
            model_name='term',
            old_name='order',
            new_name='priority',
        ),
        migrations.CreateModel(
            name='QueryLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('data', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('term', models.ForeignKey(default=None, to='course.Term')),
                ('results', models.IntegerField(default=0)),
            ],
        ),
    ]
