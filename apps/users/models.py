from datetime import datetime
from urllib import parse

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from utils.help_avatar_hash import generate_avatar_hash


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="邮箱地址", max_length=100)
    can_comment = models.BooleanField(default=True, verbose_name="能否评论")
    avatar_hash = models.CharField(verbose_name="Gravatar头像", null=True, blank=True, max_length=100)
    is_activated = models.BooleanField(default=False, verbose_name="激活用户")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.username

    def get_favourite_number(self):
        return self.userfavourite_set.all().count()

    def get_comments_number(self):
        return self.comments_set.all().count()

    def get_like_number(self):
        return self.userlike_set.all().count()

    def get_gravatar_url(self, size=100):
        return "https://www.gravatar.com/avatar/{0}?{1}".format(self.avatar_hash, parse.urlencode(
            {"d": settings.DEFAULT_GRAVATAR_STYLE, 's': str(size)}))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.email is not None and self.avatar_hash is None:
            # 如果没有保存头像哈希值，生成一个
            self.avatar_hash = generate_avatar_hash(self.email)

        # 更新修改日期
        self.update_time = datetime.now()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
