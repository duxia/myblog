# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20150228_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='commentnums',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
