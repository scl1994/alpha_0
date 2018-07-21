from django.contrib import admin

from .models import Comments, UserLike, UserFavourite


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "comment_type", "object_id", "add_time")


@admin.register(UserLike)
class UserLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "like_type", "object_id", "add_time")


@admin.register(UserFavourite)
class UserFavouriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "favourite_type", "object_id", "add_time")
