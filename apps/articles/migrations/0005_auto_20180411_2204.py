# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-11 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20180411_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='content_html',
            field=models.TextField(null=True, verbose_name='文章内容(html)'),
        ),
        migrations.AlterField(
            model_name='articles',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='articles.TagsOfArticle', verbose_name='文章标签'),
        ),
    ]
