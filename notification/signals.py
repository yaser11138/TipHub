from django.dispatch import receiver
from django_comments.signals import comment_was_posted
from django_comments_xtd.models import XtdComment
from .models import Notification


@receiver(comment_was_posted)
def create_notification(sender, comment, request, **kwargs):
    if comment.parent_id == 0:
        notification = Notification(sender=request.user)
        notification.text = "یک کامنت برای پست ارسال شد"
        url = f"{comment.content_object.get_absolute_url()}/#c{comment.xtd_comment.id}"
        notification.url = url
        notification.save()
        notification.receiver.add(comment.content_object.author)
        notification.save()
    elif comment.parent_id > 0:
        notification = Notification(sender=request.user)
        notification.text = "یک پاسخ برای کامنت   شما ارسال شد"
        url = f"{comment.content_object.get_absolute_url()}/#c{comment.xtd_comment.id}"
        notification.url = url
        reciver_user = XtdComment.objects.get(id=comment.parent_id).user
        notification.save()
        notification.receiver.add(reciver_user)
        notification.save()
