# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0055_auto_20160825_1348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='ingredients',
        ),
    ]
