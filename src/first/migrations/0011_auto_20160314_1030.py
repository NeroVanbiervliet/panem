# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-14 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0010_account_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='bakery',
            name='GPSLat',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=15),
        ),
        migrations.AddField(
            model_name='bakery',
            name='GPSLon',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=15),
        ),
    ]
