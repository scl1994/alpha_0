# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-11 12:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('image', models.ImageField(default='media/default/articles/article_01.jpg', max_length=500, upload_to='image/articles/%Y/%m', verbose_name='封面图')),
                ('abstract', models.CharField(max_length=500, verbose_name='摘要')),
                ('is_original', models.BooleanField(default=True, verbose_name='是否原创')),
                ('original_author', models.CharField(default='Anonymous', max_length=50, verbose_name='原作者')),
                ('content_markdown', models.TextField(verbose_name='文章内容(markdown)')),
                ('content_html', models.TextField(verbose_name='文章内容(html)')),
                ('click_number', models.IntegerField(default=0, verbose_name='点击量')),
                ('can_comment', models.BooleanField(default=True, verbose_name='开放评论')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='系列名')),
                ('description', models.CharField(max_length=500, verbose_name='描述')),
                ('image', models.ImageField(default='media/default/series/series_01.jpg', max_length=500, upload_to='image/series/%Y/%m', verbose_name='封面图')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '系列',
                'verbose_name_plural': '系列',
            },
        ),
        migrations.CreateModel(
            name='SpecialColumn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='专栏名')),
                ('description', models.CharField(max_length=500, verbose_name='专栏简介')),
                ('image', models.ImageField(default='media/default/specialColumn/special_01.jpg', max_length=500, upload_to='image/specialColumn/%Y/%m', verbose_name='专栏封面')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '专栏',
                'verbose_name_plural': '专栏',
            },
        ),
        migrations.CreateModel(
            name='TagsOfArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='标签名')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
    ]
