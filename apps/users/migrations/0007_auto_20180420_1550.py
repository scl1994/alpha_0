# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-20 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20180420_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_avatar',
            field=models.ImageField(default='default/avatar/avatar_01.jpg', max_length=500, upload_to='image/avatar/%Y/%m', verbose_name='用户头像'),
        ),
    ]
