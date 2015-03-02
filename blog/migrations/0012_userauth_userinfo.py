# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_login', '__first__'),
        ('blog', '0011_auto_20150222_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAuth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(unique=True, max_length=255)),
                ('password', models.CharField(max_length=128)),
                ('user', models.OneToOneField(related_name='inner_user', to='social_login.SiteUser')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=32)),
                ('avatar', models.CharField(max_length=255, blank=True)),
                ('user', models.OneToOneField(related_name='user_info', to='social_login.SiteUser')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
