# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-26 19:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_userprofile_avatar_hash'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_avatar',
        ),
    ]
