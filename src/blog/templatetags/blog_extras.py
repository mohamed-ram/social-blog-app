from django import template
from ..models import Post
from django.contrib.auth.models import User
register = template.Library()


@register.inclusion_tag(filename='blog_tags/tags.html')
def tags():
    posts = Post.objects.filter(publish=True)
    tags_list = set()
    for post in posts:
        all_tags = set(post.tags.split('-'))
        for tag in all_tags:
            tags_list.add(tag.strip())
    return {'tags_list': tags_list}


@register.inclusion_tag(filename='blog_tags/top_writers.html')
def writers_to_follow(request):
    writers = User.objects.exclude(username=request.user.username)
    return {'writers': writers, 'request': request}

