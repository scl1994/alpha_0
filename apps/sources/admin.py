from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Sources
from users.models import UserProfile


@admin.register(Sources)
class SourcesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "add_time")

    readonly_fields = ("image_show", "description_html")

    fieldsets = (
        ("基本信息", {"fields": ["name", "author", "download_url", "abstract", "can_comment"]}),
        ("图片", {"fields": ["cover_url", "image_show"]}),
        ("描述", {"fields": ["description", "description_html"]}),
        ("更多信息", {"fields": ["click_number", "add_time", "update_time"]}),
    )

    def image_show(self, obj):
        return mark_safe('<img src="{}" style="max-width: 100%" alt="picture"/>'.format(obj.cover_url))
    image_show.short_description = "封面图展示"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """根据用户的is_staff字段对资源的author外键字段进行过滤，因为只有is_staff为true才可以登录admin后台"""
        if db_field.name == "author":
            kwargs["queryset"] = UserProfile.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)