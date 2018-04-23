from datetime import datetime

from django.db import models

from users.models import UserProfile


class UserFavourite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    favourite_id = models.IntegerField(default=0, verbose_name="数据ID")
    favourite_type = models.IntegerField(choices=((1, '文章'), (2, '资源')), default=1, verbose_name="收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user) + '的收藏'


class UserLike(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    favourite_id = models.IntegerField(default=0, verbose_name="数据ID")
    favourite_type = models.IntegerField(choices=((1, '文章'), (2, '资源'), (3, '评论')), default=1, verbose_name="点赞类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "用户点赞"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user) + '的赞'
