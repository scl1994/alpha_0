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


# class EmailVerifyCode(models.Model):
#     code = models.CharField(max_length=50, verbose_name="验证码")
#     email = models.EmailField(max_length=50, verbose_name="邮箱")
#     send_type = models.CharField(verbose_name="验证码类型", choices=(("register", "注册"), ("forget_pwd", "找回密码"),
#                                                                 ("update_email", "修改邮箱")), max_length=20)
#     send_time = models.DateTimeField(verbose_name="发送时间", default=datetime.now)
#     expiration = models.IntegerField(verbose_name="有效时间(秒)", default=3600)
#     be_used = models.BooleanField(default=True, verbose_name='是否可用')
#
#     class Meta:
#         verbose_name = "邮箱验证码"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return '{0}({1})'.format(self.code, self.email)
