from django.contrib import admin
from .models import Post, Comment,Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('slug', 'user', 'created', 'updated')
    prepopulated_fields = {'slug': ('body',)}
    list_filter = ('updated',)
    search_fields = ('slug', 'body')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'created')
    raw_id_fields = ('user', 'reply', 'post')


admin.site.register(Like)
