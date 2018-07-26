from datetime import datetime

from django.db import models
from django.conf import settings
import markdown2

from users.models import UserProfile
from user_operations.models import UserLike, UserFavourite, Comments


class Sources(models.Model):
    name = models.CharField(max_length=200, verbose_name="资源名称")
    author = models.ForeignKey(UserProfile, verbose_name="添加人", on_delete=models.CASCADE)
    download_url = models.URLField(max_length=500, verbose_name="下载地址")
    abstract = models.CharField(max_length=500, verbose_name="简介")
    cover_url = models.URLField(max_length=500, verbose_name="封面图",
                                default=settings.DEFAULT_SOURCE_URL)
    description = models.TextField(verbose_name="详细介绍")
    description_html = models.TextField(verbose_name="详细介绍（html）", default="", null=True, blank=True)
    can_comment = models.BooleanField(default=True, verbose_name="能否评论")
    click_number = models.IntegerField(default=0, verbose_name="点击量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "资源"
        verbose_name_plural = "资源"

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            self.description_html = markdown2.markdown(self.description, extras=[
                'fenced-code-blocks',
                'cuddled-lists',
                'tables',
                'code-friendly'])
        except Exception:
            self.description_html = self.description
        # 更新修改日期
        self.update_time = datetime.now()

        super(Sources, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def get_favourite_number(self):
        favourite_number = UserFavourite.objects.filter(object_id=self.id, favourite_type=2).count()
        return favourite_number

    def get_like_number(self):
        like_number = UserLike.objects.filter(object_id=self.id, like_type=2).count()
        return like_number

    def get_comment_number(self):
        comment_number = Comments.objects.filter(object_id=self.id, comment_type=2).count()
        return comment_number
