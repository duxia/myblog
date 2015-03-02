# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150203_2036'),
    ]

    operations = [
        migrations.CreateModel(
            name='articletypeList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typename', models.CharField(max_length=30)),
                ('articleNums', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='article',
            name='articletype',
            field=models.ForeignKey(to='blog.articletypeList'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='publishdate',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
