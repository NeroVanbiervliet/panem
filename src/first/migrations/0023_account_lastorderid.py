# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-10 20:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0022_auto_20160508_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='lastOrderId',
            field=models.IntegerField(default=0),
        ),
    ]
