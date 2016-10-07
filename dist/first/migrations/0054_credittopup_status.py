# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0053_adyenpayment_iscredittopup'),
    ]

    operations = [
        migrations.AddField(
            model_name='credittopup',
            name='status',
            field=models.CharField(default='created', max_length=100),
        ),
    ]
