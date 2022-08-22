from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_jalali.db import models as jmodels
from jdatetime import datetime
User = get_user_model()


def blog_video_path(instance, filename):
    return f"user_{instance.author.id}/post_{instance.pk}/video/{filename}"


def blog_video_thumbnail_path(instance, filename):
    return f"user_{instance.author.id}/post_{instance.pk}/video/thumbnail/{filename}"


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS = (
        ("draft", 'Draft'),
        ("published", 'Published')
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    title = models.CharField(max_length=250)
    body = models.TextField()
    video = models.FileField(upload_to=blog_video_path)
    video_thumbnail = models.ImageField(upload_to=blog_video_thumbnail_path, null=True)
    publish = jmodels.jDateTimeField(default=datetime.now())
    created = jmodels.jDateTimeField(auto_now_add=True)
    upadated = jmodels.jDateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS, default='draft')
    objects = jmodels.jManager()
    published = PublishedManager()


