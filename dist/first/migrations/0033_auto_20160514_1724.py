# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-14 17:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0032_auto_20160514_1721'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='time_ordered',
            new_name='timeOrdered',
        ),
    ]
