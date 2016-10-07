# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0049_auto_20160811_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='bakery',
            name='emailNotifyNextDayOrder',
            field=models.BooleanField(default=True),
        ),
    ]
