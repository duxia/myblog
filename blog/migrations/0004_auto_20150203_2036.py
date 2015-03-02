# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150203_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publishdate',
            field=models.DateField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
