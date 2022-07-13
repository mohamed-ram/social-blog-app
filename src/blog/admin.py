from django.contrib import admin
from django import forms
from .models import Category, Post, Comment
# Register your models here.


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"


class PostAdmin(admin.ModelAdmin):
    fields = ['author', 'title', 'slug', 'image', 'text', 'category', 'tags', 'publish_at', 'publish']
    list_display = ('title', 'created_at', 'category', 'publish_at', 'author', 'publish')
    list_filter = ['author', 'publish_at', 'publish']
    date_hierarchy = 'created_at'
    search_fields = ['title', 'text']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    ordering = ['publish_at']


admin.site.register(Post, PostAdmin)
admin.site.register(Category)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created', 'updated', 'active']
    list_filter = ['name', 'email', 'active']
    date_hierarchy = 'created'
    search_fields = ['name', 'title', 'comment']
    ordering = ['created']


admin.site.register(Comment, CommentAdmin)

