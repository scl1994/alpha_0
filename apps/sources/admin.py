from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Sources


@admin.register(Sources)
class SourcesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "add_time")

    readonly_fields = ("image_show",)

    def image_show(self, obj):
        return mark_safe('<img src="{}" style="max-width: 100%" alt="picture"/>'.format(obj.image.url))
    image_show.short_description = "封面图展示"
