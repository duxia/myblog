# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20150203_2045'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': '\u6587\u7ae0', 'verbose_name_plural': '\u6587\u7ae0'},
        ),
        migrations.AlterModelOptions(
            name='articletypelist',
            options={'verbose_name': '\u6587\u7ae0\u7c7b\u578b', 'verbose_name_plural': '\u6587\u7ae0\u7c7b\u578b'},
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name=b'content'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='publishdate',
            field=models.DateField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
