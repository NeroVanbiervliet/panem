# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-05 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0020_auto_20160501_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='salt',
            field=models.CharField(default='', max_length=200),
        ),
    ]
