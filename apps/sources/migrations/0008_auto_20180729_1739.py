# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-29 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0007_auto_20180726_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sources',
            name='cover_url',
            field=models.URLField(default='https://alpha-pics-1256464384.cos.ap-shanghai.myqcloud.com/default%2Fsources%2Fsources_01.jpg', max_length=500, verbose_name='封面图'),
        ),
    ]