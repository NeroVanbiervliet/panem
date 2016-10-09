# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0050_bakery_emailnotifynextdayorder'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditTopUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accountId', models.IntegerField(default=0)),
                ('timeOrdered', models.DateTimeField()),
                ('amountToPay', models.IntegerField(default=0)),
                ('amountTopUp', models.IntegerField(default=0)),
            ],
        ),
    ]
