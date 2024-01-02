from django.contrib import admin

from api.models import Comment, Post


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "body", "email", "name", "post",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "body", "title", "user_id",)
