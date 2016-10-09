# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0054_credittopup_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='bakeryId',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='isStandard',
            field=models.BooleanField(default=True),
        ),
    ]
