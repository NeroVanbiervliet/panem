# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-13 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0008_auto_20160312_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='adress',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='account',
            name='city',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='account',
            name='password',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='account',
            name='postcode',
            field=models.IntegerField(default=0),
        ),
    ]
