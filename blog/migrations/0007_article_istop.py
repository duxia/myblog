# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20150208_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='istop',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
