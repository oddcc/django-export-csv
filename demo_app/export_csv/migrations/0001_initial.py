# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name="College's name", max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name="Student's name", max_length=30)),
                ('age', models.IntegerField(verbose_name="Student's age")),
                ('is_graduated', models.BooleanField(verbose_name='Graduated', default=False)),
                ('birthday', models.DateTimeField(verbose_name='Birthday')),
                ('college', models.ForeignKey(verbose_name="Students's college", to='export_csv.College')),
            ],
        ),
    ]
