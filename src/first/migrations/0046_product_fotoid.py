# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-04 11:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0045_auto_20160704_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='fotoId',
            field=models.IntegerField(default=0),
        ),
    ]
