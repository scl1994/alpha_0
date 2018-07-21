from django.contrib import admin
from django.utils.safestring import mark_safe

from users.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')
    list_display = ("id", "username")
    readonly_fields = ('avatar_image', 'password')
    fieldsets = (
        ("基本信息", {"fields": ["username", "email", "add_time", "update_time"]}),
        ("图片", {"fields": ["avatar_image", "user_avatar"]}),
        ("权限", {"fields": ["is_superuser", "is_staff", "is_activated", "is_active", "can_comment", "groups",
                           "user_permissions"]}))

    def avatar_image(self, obj):
        return mark_safe('<img src="{}" style="max-width: 100%" alt="picture"/>'.format(obj.user_avatar.url))

    avatar_image.short_description = '头像图片'


# 用来更改后台管理系统的名称和浏览器显示标题
admin.site.site_header = "Alpha博客管理系统"
admin.site.site_title = "Alpha后台管理系统"
