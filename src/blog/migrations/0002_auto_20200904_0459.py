# Generated by Django 3.1.1 on 2020-09-04 02:59

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='post',
            managers=[
                ('upcoming', django.db.models.manager.Manager()),
            ],
        ),
    ]
