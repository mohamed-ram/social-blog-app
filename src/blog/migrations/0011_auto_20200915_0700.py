# Generated by Django 3.1.1 on 2020-09-15 05:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20200915_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 15, 5, 0, 32, 740755, tzinfo=utc)),
        ),
    ]