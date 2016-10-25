# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0059_promocode_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='credittopup',
            name='promoCodeId',
            field=models.IntegerField(default=0),
        ),
    ]
