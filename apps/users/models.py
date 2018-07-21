from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="邮箱地址", max_length=100)
    can_comment = models.BooleanField(default=True, verbose_name="能否评论")
    user_avatar = models.ImageField(upload_to="image/avatar/%Y/%m", max_length=500,
                                    default="avatar/avatar_01.jpg", verbose_name="用户头像")
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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 更新修改日期
        self.update_time = datetime.now()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
