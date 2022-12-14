# Generated by Django 4.1 on 2022-09-01 23:31

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_alter_teacher_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="teacher",
            options={"verbose_name": "Teacher", "verbose_name_plural": "Teachers"},
        ),
        migrations.AlterField(
            model_name="customuser",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, region=None, verbose_name="Phone Number"
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="profile_picture",
            field=models.ImageField(
                default="sutdent-prof.png",
                upload_to=accounts.models.profile_picture_path,
                verbose_name="Profile Picture",
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="bio",
            field=models.TextField(verbose_name="Bio"),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="github",
            field=models.URLField(blank=True, null=True, verbose_name="github"),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="instagram",
            field=models.URLField(blank=True, null=True, verbose_name="Instagram"),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="linkedin",
            field=models.URLField(blank=True, null=True, verbose_name="linkedin"),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="telegram",
            field=models.URLField(blank=True, null=True, verbose_name="telegram"),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
    ]
