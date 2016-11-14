# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0058_promocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='code',
            field=models.CharField(default='', max_length=15),
        ),
    ]
