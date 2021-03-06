# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-11 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_avatar',
            field=models.ImageField(default='media/default/avatar/avatar_01.jpg', max_length=500, upload_to='image/avatar/%Y/%m', verbose_name='用户头像'),
        ),
    ]
