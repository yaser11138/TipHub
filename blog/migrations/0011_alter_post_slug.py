# Generated by Django 4.1 on 2022-08-31 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0010_remove_post_noww"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(allow_unicode=True, max_length=250),
        ),
    ]
