# Generated by Django 4.1 on 2022-09-05 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0021_post_tags"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="categories",
            new_name="category",
        ),
    ]
