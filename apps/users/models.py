from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    can_comment = models.BooleanField(default=True, verbose_name="能否评论")
    user_avatar = models.ImageField(upload_to="image/avatar/%Y/%m", max_length=500,
                                    default="media/default/avatar/avatar_01.jpg", verbose_name="用户头像")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.username
