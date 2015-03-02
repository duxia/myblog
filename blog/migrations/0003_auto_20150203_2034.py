# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150203_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publishdate',
            field=models.DateField(auto_now=True),
            preserve_default=True,
        ),
    ]
