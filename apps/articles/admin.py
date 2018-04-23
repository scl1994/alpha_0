from datetime import datetime

from django.contrib import admin
from django.utils.safestring import mark_safe

from articles.models import TagsOfArticle, SpecialColumn, Series, Articles


@admin.register(TagsOfArticle)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "add_time",)
    fieldsets = (
        ("基本信息", {"fields": ["name"]}),
        ("日期", {"fields": ["add_time", "update_time"]}),
    )


@admin.register(SpecialColumn)
class SpecialColumnAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "add_time",)
    readonly_fields = ("image_show",)
    fieldsets = (
        ("基本信息", {"fields": ["title", "description"]}),
        ("图片", {"fields": ["image_show", "image"]}),
        ("日期", {"fields": ["add_time", "update_time"]}),
    )

    def image_show(self, obj):
        return mark_safe('<img src={} style="max-width: 100%" alt="picture">'.format(obj.image.url))

    image_show.short_description = '封面'


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "add_time",)

    # 必须将展示图片的字段设置为只读
    readonly_fields = ("image_show",)
    fieldsets = (
        ("基本信息", {"fields": ["title", "description"]}),
        ("图片", {"fields": ["image_show", "image"]}),
        ("日期", {"fields": ["add_time", "update_time"]}),
        )

    # 用于在后台显示图片（默认的图片字段是一个路径，显示不了图片）
    def image_show(self, obj):
        return mark_safe('<img src={} style="max-width: 100%" alt="picture">'.format(obj.image.url))

    image_show.short_description = '封面'


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "click_number", "add_time", "update_time")
    search_fields = ('id', 'title', 'author',)
    list_filter = ("is_original", "can_comment", "special_column", "tags")
    filter_horizontal = ('tags',)
    readonly_fields = ("image_show", "content_html", "click_number", "add_time", "update_time")
    exclude = ("content_html",)
    fieldsets = (
        ("基本信息", {"fields": ["title", "abstract", "author", "can_comment", "special_column", "series", "tags"]}),
        ("图片", {"fields": ["image_show", "image"]}),
        ("文章主体", {"fields": ["content_markdown", "content_html"]}),
        ("更多信息", {"fields": ["is_original", "original_author", "click_number", "add_time", "update_time"]}),
    )

    def image_show(self, obj):
        return mark_safe('<img src={} style="max-width: 100%" alt="picture">'.format(obj.image.url))

    image_show.short_description = '封面'

    # def save_model(self, request, obj, form, change):
    #     if change:
    #         obj.update_time = datetime.now()
    #
    #     super().save_model(request, obj, form, change)
