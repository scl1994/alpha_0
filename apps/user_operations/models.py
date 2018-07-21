from datetime import datetime

from django.db import models

from users.models import UserProfile


class UserFavourite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    object_id = models.IntegerField(default=0, verbose_name="对象ID")
    favourite_type = models.IntegerField(choices=((1, '文章'), (2, '资源')), default=1, verbose_name="收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user) + '的收藏'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 更新修改日期
        self.update_time = datetime.now()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class UserLike(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    object_id = models.IntegerField(default=0, verbose_name="对象ID")
    like_type = models.IntegerField(choices=((1, '文章'), (2, '资源'), (3, '评论')), default=1, verbose_name="点赞类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "用户点赞"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user) + '的赞'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 更新修改日期
        self.update_time = datetime.now()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Comments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    content = models.CharField(max_length=500, verbose_name="评论内容")
    comment_type = models.IntegerField(choices=((1, "文章评论"), (2, "资源评论")), default=1, verbose_name="评论类型")
    object_id = models.IntegerField(verbose_name="对象ID")
    # like_number = models.IntegerField(default=0, verbose_name="赞数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"

    def __str__(self):
        return str(self.user) + '的评论'

    def get_like_number(self):
        like_number = UserLike.objects.filter(object_id=self.id, like_type=3).count()
        return like_number

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 更新修改日期
        self.update_time = datetime.now()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
