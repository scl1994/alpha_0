from django.contrib import admin

from articles.models import TagsOfArticle, SpecialColumn, Series, Articles


@admin.register(TagsOfArticle)
class TagsAdmin(admin.ModelAdmin):
    pass


@admin.register(SpecialColumn)
class SpecialColumnAdmin(admin.ModelAdmin):
    pass


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    pass


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "click_number", "add_time", "update_time")
    search_fields = ('id', 'title', 'author',)
    list_filter = ("id", "title", "click_number")
    filter_horizontal = ('tags',)
    readonly_fields = ("content_html",)