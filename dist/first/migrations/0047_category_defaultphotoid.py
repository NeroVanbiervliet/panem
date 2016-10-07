# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0046_product_fotoid'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='defaultPhotoId',
            field=models.IntegerField(default=0),
        ),
    ]
