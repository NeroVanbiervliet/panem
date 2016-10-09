# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0047_category_defaultphotoid'),
    ]

    operations = [
        migrations.AddField(
            model_name='bakery',
            name='photoId',
            field=models.IntegerField(default=0),
        ),
    ]
