# Generated by Django 4.1 on 2022-08-22 08:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog_post", "0007_alter_post_publish"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="publish",
            field=django_jalali.db.models.jDateTimeField(
                default=datetime.datetime(2022, 8, 22, 12, 51, 30, 903355)
            ),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("created", django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ("updated", django_jalali.db.models.jDateTimeField(auto_now=True)),
                ("active", models.BooleanField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="blog_post.comment",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="blog_post.post",
                    ),
                ),
            ],
            options={
                "ordering": ("-created",),
            },
        ),
    ]
