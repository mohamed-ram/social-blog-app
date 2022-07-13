# Generated by Django 3.1.1 on 2020-09-13 03:50

import account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=70, null=True)),
                ('image', models.ImageField(blank=True, upload_to=account.models.save_image_to)),
                ('fb_url', models.URLField(blank=True, null=True)),
                ('tw_url', models.URLField(blank=True, null=True)),
                ('in_url', models.URLField(blank=True, null=True)),
                ('yt_url', models.URLField(blank=True, null=True)),
                ('website_url', models.URLField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]