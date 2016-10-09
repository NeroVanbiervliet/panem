# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0051_credittopup'),
    ]

    operations = [
        migrations.RenameField(
            model_name='credittopup',
            old_name='timeOrdered',
            new_name='dateOrdered',
        ),
    ]
