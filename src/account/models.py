from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from blog.models import Post


def save_image_to(instance, file_name):
    extension = file_name.split('.')[-1]
    return f"users/{instance.user.username}.{extension.lower()}"


def save_file_to(instance, file_name):
    extension = file_name.split('.')[-1]
    return f"cvs/{instance.user.username}.{extension.lower()}"


class ProfileManager(models.Manager):
    def all(self):
        qs = self.get_queryset().all()
        if self.instance:
            qs = self.exclude(user=self.instance)
        return qs


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by')
    description = models.CharField(max_length=70, null=True, blank=True)
    bio = RichTextField(blank=True)
    image = models.ImageField(upload_to=save_image_to, blank=True)
    cv = models.FileField(upload_to=save_file_to, blank=True, null=True)
    fb_url = models.URLField(blank=True, null=True)
    tw_url = models.URLField(blank=True, null=True)
    in_url = models.URLField(blank=True, null=True)
    yt_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)

    objects = ProfileManager()

    def get_following(self):
        users = self.following.all()
        return users.exclude(username=self.user.username)

    def __str__(self):
        return f'{self.user}\'s profile'


