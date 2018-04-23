from django.contrib import admin
from django.utils.safestring import mark_safe

from users.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fields = ("username", "email", 'avatar_image', "user_avatar", "is_activated", "can_comment",
              "add_time", "update_time")
    list_display = ("id", "username")
    readonly_fields = ('avatar_image', 'password')

    def avatar_image(self, obj):
        return mark_safe('<img src="{}" style="max-width: 100%" alt="picture"/>'.format(obj.user_avatar.url))

    avatar_image.short_description = '品牌图片'
