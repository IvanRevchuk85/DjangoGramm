from django.contrib import admin
from .models import Post, PostImage, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'image')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
