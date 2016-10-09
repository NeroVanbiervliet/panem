# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0052_auto_20160819_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='adyenpayment',
            name='isCreditTopUp',
            field=models.BooleanField(default=False),
        ),
    ]
