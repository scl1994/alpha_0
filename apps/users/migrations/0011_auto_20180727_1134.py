# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-27 11:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_userprofile_user_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='is_activated',
            new_name='confirmed',
        ),
    ]
