# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20160213_2009'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Prices',
            new_name='Price',
        ),
        migrations.RenameModel(
            old_name='Services',
            new_name='Service',
        ),
    ]
