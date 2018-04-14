from django.contrib import admin
from django.utils.safestring import mark_safe

from users.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "username")
    readonly_fields = ('avatar_image',)

    def avatar_image(self, obj):
        return mark_safe(u'<img src="{}" width="100px"/>'.format(obj.user_avatar.url))

    avatar_image.short_description = '品牌图片'
