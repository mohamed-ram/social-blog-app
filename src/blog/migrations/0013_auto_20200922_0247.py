# Generated by Django 3.1.1 on 2020-09-22 00:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20200922_0243'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='text',
            new_name='comment',
        ),
        migrations.AlterField(
            model_name='post',
            name='publish_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 22, 0, 46, 58, 475379, tzinfo=utc)),
        ),
    ]
