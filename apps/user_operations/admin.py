from django.contrib import admin

from .models import Comments


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "add_time")

