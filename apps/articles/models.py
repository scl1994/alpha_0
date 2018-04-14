from datetime import datetime

from django.db import models
import markdown

from users.models import UserProfile


class TagsOfArticle(models.Model):
    name = models.CharField(max_length=50, verbose_name="标签名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SpecialColumn(models.Model):
    title = models.CharField(max_length=50, verbose_name="专栏名")
    description = models.CharField(max_length=500, verbose_name="专栏简介")
    image = models.ImageField(upload_to="image/specialColumn/%Y/%m", max_length=500,
                              default="media/default/specialColumn/special_01.jpg", verbose_name="专栏封面")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "专栏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Series(models.Model):
    title = models.CharField(max_length=50, verbose_name="系列名")
    description = models.CharField(max_length=500, verbose_name="描述")
    image = models.ImageField(upload_to="image/series/%Y/%m", max_length=500,
                              default="media/default/series/series_01.jpg", verbose_name="封面图")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "系列"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Articles(models.Model):
    title = models.CharField(max_length=200, verbose_name="标题")
    image = models.ImageField(upload_to="image/articles/%Y/%m", max_length=500,
                              default="media/default/articles/article_01.jpg", verbose_name="封面图")
    author = models.ForeignKey(UserProfile, verbose_name="作者")
    abstract = models.CharField(max_length=500, verbose_name="摘要")
    special_column = models.ForeignKey(SpecialColumn, verbose_name="专栏")
    tags = models.ManyToManyField(TagsOfArticle, blank=True, verbose_name="文章标签")
    series = models.ForeignKey(Series, null=True, blank=True, verbose_name="文章系列")
    is_original = models.BooleanField(default=True, verbose_name="是否原创")
    original_author = models.CharField(max_length=50, default="Anonymous", verbose_name="原作者")
    content_markdown = models.TextField(verbose_name="文章内容(markdown)")
    content_html = models.TextField(null=True, verbose_name="文章内容(html)")
    click_number = models.IntegerField(default=0, verbose_name="点击量")
    can_comment = models.BooleanField(default=True, verbose_name="开放评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            self.content_html = markdown.markdown(self.content_markdown, extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc', ])
        except Exception:
            self.content_html = self.content_markdown

        super(Articles, self).save()
