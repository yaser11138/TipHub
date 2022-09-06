# Generated by Django 4.1 on 2022-09-04 12:17

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0015_category_post_categories"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                allow_unicode=True,
                editable=False,
                populate_from="name",
                unique_with=("parent_category",),
            ),
        ),
    ]
