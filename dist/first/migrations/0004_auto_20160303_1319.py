# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-03 13:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0003_auto_20160303_1127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bakery',
            old_name='openingsuren',
            new_name='openings',
        ),
    ]
