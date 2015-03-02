# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_article_istop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='clicknums',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articletypelist',
            name='articleNums',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
