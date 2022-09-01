from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.text import slugify
from .models import Post
from jdatetime import date


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "body", "video", "video_thumbnail", "status", "enable_comments")
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "یک پست با این عنوان در حال حاضر در سایت وجود دارد ",
            }
        }

    def save(self, commit=True):
        post = super(PostForm, self).save(commit=False)
        if post.slug == "":
            post.slug = slugify(post.title, allow_unicode=True)
        if post.publish is None and post.status == "published":
            post.publish = date.today()
        if commit:
            post.save()
        return post
