# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-04 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0044_delete_disabledateslol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bakery',
            name='foto_url',
        ),
        migrations.RemoveField(
            model_name='product',
            name='foto_url',
        ),
        migrations.AlterField(
            model_name='hasproduct',
            name='availability',
            field=models.BooleanField(default=False),
        ),
    ]
