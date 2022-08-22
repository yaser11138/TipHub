# Generated by Django 4.1 on 2022-08-21 07:48

import datetime
from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ("blog_post", "0002_post_video_thumbnail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="created",
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="publish",
            field=django_jalali.db.models.jDateTimeField(
                default=datetime.datetime(2022, 8, 21, 12, 18, 25, 954666)
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="upadated",
            field=django_jalali.db.models.jDateTimeField(auto_now=True),
        ),
    ]
