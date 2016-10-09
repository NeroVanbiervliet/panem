# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0048_bakery_photoid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='fotoId',
            new_name='photoId',
        ),
    ]
