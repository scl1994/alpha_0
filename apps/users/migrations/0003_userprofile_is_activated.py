# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-14 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180411_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_activated',
            field=models.BooleanField(default=False, verbose_name='激活用户'),
        ),
    ]
