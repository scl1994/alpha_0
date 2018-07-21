from datetime import datetime

from django.db import models
import markdown2

from users.models import UserProfile
from user_operations.models import Comments, UserLike, UserFavourite


class TagsOfArticle(models.Model):
    name = models.CharField(max_length=50, verbose_name="标签名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 更新修改日期
        self.update_time = datetime.now()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class SpecialColumn(models.Model):
    title = models.CharField(max_length=50, verbose_name="专栏名")
    description = models.CharField(max_length=500, verbose_name="专栏简介")
    image = models.ImageField(upload_to="image/specialColumn/%Y/%m", max_length=500,
                              default="default/specialColumn/special_01.jpg", verbose_name="专栏封面")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "专栏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_articles(self):
        return self.articles_set.all()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 更新修改日期
        self.update_time = datetime.now()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Series(models.Model):
    title = models.CharField(max_length=50, verbose_name="系列名")
    description = models.CharField(max_length=500, verbose_name="描述")
    image = models.ImageField(upload_to="image/series/%Y/%m", max_length=500,
                              default="default/series/series_01.jpg", verbose_name="封面图")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "系列"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_articles(self):
        return self.articles_set.all()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 更新修改日期
        self.update_time = datetime.now()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Articles(models.Model):
    title = models.CharField(max_length=200, verbose_name="标题")
    image = models.ImageField(upload_to="image/articles/%Y/%m", max_length=500,
                              default="default/articles/article_01.jpg", verbose_name="封面图")
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
    # favourite_number = models.IntegerField(default=0, verbose_name="收藏数")
    # like_number = models.IntegerField(default=0, verbose_name="赞数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_favourite_number(self):
        favourite_number = UserFavourite.objects.filter(object_id=self.id, favourite_type=1).count()
        return favourite_number

    def get_like_number(self):
        like_number = UserLike.objects.filter(object_id=self.id, like_type=1).count()
        return like_number

    def get_comment_number(self):
        comment_number = Comments.objects.filter(object_id=self.id, comment_type=1).count()
        return comment_number

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            self.content_html = markdown2.markdown(self.content_markdown, extras=[
                'fenced-code-blocks',
                'cuddled-lists',
                'tables',
                'code-friendly'])
        except Exception:
            self.content_html = self.content_markdown
        # 更新修改日期
        self.update_time = datetime.now()

        super(Articles, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def get_tags_string(self):
        tags = [tag.name for tag in self.tags.all()]
        return ",".join(tags)
