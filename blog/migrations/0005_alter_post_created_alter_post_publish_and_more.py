# Generated by Django 4.1 on 2022-08-29 14:14

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_alter_post_created_alter_post_slug"),
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
            field=django_jalali.db.models.jDateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="upadated",
            field=django_jalali.db.models.jDateTimeField(auto_now=True),
        ),
    ]
