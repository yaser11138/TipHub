# Generated by Django 4.1 on 2022-08-29 13:26

import blog.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_alter_post_publish"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="video_thumbnail",
            field=models.ImageField(
                upload_to=blog.models.blog_video_thumbnail_path,
                validators=[django.core.validators.validate_image_file_extension],
            ),
        ),
    ]
