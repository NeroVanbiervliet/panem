# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-03 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0040_auto_20160703_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisableDates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bakeryId', models.IntegerField(default=0)),
                ('date', models.DateTimeField(default=0)),
            ],
        ),
    ]
