# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-12 18:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0007_auto_20160304_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='bakery',
            name='city',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='bakery',
            name='postcode',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='standard',
            field=models.IntegerField(default=0),
        ),
    ]
