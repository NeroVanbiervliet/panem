# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-25 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0017_auto_20160425_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bakery',
            name='openings',
            field=models.CharField(default='', max_length=600),
        ),
    ]
