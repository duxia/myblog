# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': '\u8bc4\u8bba', 'verbose_name_plural': '\u8bc4\u8bba'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', blank=True, to='blog.comment', null=True),
            preserve_default=True,
        ),
    ]
