import re
import cv2
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.core.validators import FileExtensionValidator, validate_image_file_extension
from django.template import loader
from django.shortcuts import redirect
from django_comments.models import Comment
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.conf import settings
from django_comments_xtd.moderation import moderator
from django_comments.moderation import CommentModerator, get_current_site, send_mail
from django_comments_xtd import views
from django_comments_xtd.models import XtdComment
from django_jalali.db import models as jmodels
from hitcount.models import HitCount, HitCountMixin
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase
from jdatetime import datetime, timedelta
from autoslug import AutoSlugField
now = datetime.now().strftime("%Y/%m/%d")
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("name"))
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


# remove_sepical_characters of text for create folder
def remove_sepical_characters(text):
    pattern = r'[^A-Za-z0-9]+'
    return re.sub(pattern, '', text)


def blog_video_path(instance, filename):
    title = remove_sepical_characters(instance.title)
    return f"user_{instance.author.id}/{now}/{title}/video/{filename}"


def blog_video_thumbnail_path(instance, filename):
    title = remove_sepical_characters(instance.title)
    return f"user_{instance.author.id}/{now}/{title}/video/thumbnail/{filename}"


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class MyCustomTag(TagBase):
    name = models.CharField(
        verbose_name=_("name"), unique=True, max_length=100
    )
    slug = models.SlugField(
        verbose_name=_("slug"),
        unique=True,
        max_length=100,
        allow_unicode=True,
    )
    categories = models.ManyToManyField(verbose_name=_("categories"), to=Category, blank=True, related_name="tags")

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class TaggedPost(GenericTaggedItemBase):

    tag = models.ForeignKey(
        MyCustomTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

    class Meta:
        verbose_name = _("tagged item")
        verbose_name_plural = _("tagged items")
        app_label = "blog"
        index_together = [["content_type", "object_id"]]
        unique_together = [["content_type", "object_id", "tag"]]


class Post(models.Model, HitCountMixin):
    objects = jmodels.jManager()
    STATUS = (
        ("draft", 'Draft'),
        ("published", 'Published')
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts", verbose_name=_("author"))
    title = models.CharField(max_length=250, verbose_name=_("title"))
    slug = models.SlugField(max_length=250, allow_unicode=True, verbose_name=_("slug"))
    body = models.TextField(verbose_name=_("body"))
    category = models.ForeignKey(Category, related_name="posts",on_delete=models.SET_NULL, null=True)
    video = models.FileField(upload_to=blog_video_path, validators=[FileExtensionValidator(['mp4'])],
                             verbose_name=_("video"))
    video_thumbnail = models.ImageField(upload_to=blog_video_thumbnail_path,
                                        validators=[validate_image_file_extension], verbose_name=_("video_thumbnail"))
    status = models.CharField(max_length=10, choices=STATUS, default='draft', verbose_name=_('status'))
    publish = jmodels.jDateField(null=True, blank=True, verbose_name=_("publish"))
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_("created"))
    upadated = jmodels.jDateTimeField(auto_now=True, verbose_name=_("updated"))
    likes = models.ManyToManyField(User, blank=True, verbose_name=_("likes"))
    comments = GenericRelation(Comment, object_id_field="object_pk")
    # hit count for views
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')
    tags = TaggableManager(verbose_name=_("tags"), through=TaggedPost)
    published = PublishedManager()
    enable_comments = models.BooleanField(default=True, verbose_name=_("enable_comments"))

    class Meta:
        unique_together = ["slug", "publish"]
        ordering = ('-publish',)
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    @property
    def get_video_duration(self):
        video_path = self.video.path
        # create video capture object
        data = cv2.VideoCapture(video_path)
        # count the number of frames
        frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = data.get(cv2.CAP_PROP_FPS)
        # calculate duration of the video
        seconds = round(frames / fps)
        video_time = timedelta(seconds=seconds)
        return video_time

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/blog/post/{self.publish.year}/{self.publish.month}/{self.publish.day}/{self.slug}"


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
