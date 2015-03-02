# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20150222_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='usericon',
            field=models.ImageField(upload_to=b'usericons'),
            preserve_default=True,
        ),
    ]
