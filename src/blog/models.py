from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse
from ckeditor.fields import RichTextField
from django.db.models import Q



def save_image_to(instance, file_name):
    extension = file_name.split('.')[-1]
    return f"blog/{instance.slug}.{extension.lower()}"

#
# class UpComingManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(Q(publish_at__gt=timezone.now()))
#
#
# class DraftManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(Q(publish=True))

#
# class PublishManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(Q(publish=True) & Q(publish_at__lt=timezone.now()))


class PostQueryset(models.QuerySet):
    def upcoming(self):
        return self.filter(Q(publish=True) & Q(publish_at__gt=timezone.now()))


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQueryset(self.model, using=self._db)

    def all_posts(self):
        return self.all()

    def published(self):
        return self.filter(Q(publish=True) & Q(publish_at__lte=timezone.now()))

    # [1] use this or objects.get_queryset().upcoming()
    # def up_coming(self):
    #     return self.filter(Q(publish=True) & Q(publish_at__gt=timezone.now()))
    # [2] use self.queryset().upcoming()
    # def up_coming(self):
    #     return self.get_queryset().upcoming()

    def draft(self):
        return self.filter(publish=False)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=save_image_to)
    text = RichTextField()
    publish_at = models.DateTimeField(default=timezone.now())
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique_for_date='created_at', unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = models.CharField(max_length=100, default='')
    publish = models.BooleanField(default=True)

    # post manager..
    objects = PostManager()

    class Meta:
        ordering = ['-publish_at']

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # name = models.CharField(max_length=25)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    comment = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"comment form {self.name} on {self.post}"

