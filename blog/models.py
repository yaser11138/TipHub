from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext as _
from django_comments_xtd.moderation import moderator
from django_comments.moderation import CommentModerator, get_current_site, send_mail
from django_comments_xtd import views
from django.template import loader
from django.shortcuts import redirect
from django.conf import settings
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
    likes = models.ManyToManyField(User)
    objects = jmodels.jManager()
    published = PublishedManager()
    enable_comments = models.BooleanField(default=True)

    ordering = ("-publish",)

    def get_absolute_url(self):
        return f"/blog/post/{self.id}"


class PostModerator(CommentModerator):
    email_notification = True
    enable_field = 'enable_comments'

    def email(self, comment, content_object, request):
        """
        Send email notification of a new comment to post author when email
        notifications have been requested.

        """
        if not self.email_notification:
            return
        if comment.parent_id == 0:
            author_email = content_object.author.email
            recipient_list = [author_email]

        elif comment.parent_id > 0:
            author_email = XtdComment.objects.get(id=comment.parent_id).email
            recipient_list = [author_email]

        t = loader.get_template('comments/comment_notification_email.txt')
        c = {
            'comment': comment,
            'content_object': content_object,
        }
        subject = _('[%(site)s] New comment posted on "%(object)s"') % {
            'site': get_current_site(request).name,
            'object': content_object,
        }
        message = t.render(c)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


moderator.register(model_or_iterable=Post, moderation_class=PostModerator)
