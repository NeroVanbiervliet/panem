# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0060_credittopup_promocodeid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adyenpayment',
            name='extraCredit',
        ),
        migrations.RemoveField(
            model_name='credittopup',
            name='amountTopUp',
        ),
        migrations.AddField(
            model_name='adyenpayment',
            name='topUpId',
            field=models.IntegerField(default=-1),
        ),
    ]
