# Generated by Django 4.1 on 2022-09-03 12:13

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0012_alter_post_options_alter_post_author_alter_post_body_and_more"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="post",
            managers=[
                ("published", django.db.models.manager.Manager()),
            ],
        ),
    ]
