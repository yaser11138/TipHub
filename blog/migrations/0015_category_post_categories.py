# Generated by Django 4.1 on 2022-09-04 10:37

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0014_alter_post_managers"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=10, verbose_name="نام")),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False,
                        populate_from="name",
                        unique_with=("parent_category",),
                    ),
                ),
                (
                    "parent_category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="sub_categories",
                        to="blog.category",
                        verbose_name="parent categories",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="post",
            name="categories",
            field=models.ManyToManyField(related_name="posts", to="blog.category"),
        ),
    ]
