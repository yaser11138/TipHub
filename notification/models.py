from django.db import models
from django.contrib.auth import get_user_model
from blog.models import Post
User = get_user_model()


class Notification(models.Model):
    sender = models.ForeignKey(User, related_name="notifications_sent", on_delete=models.CASCADE)
    text = models.TextField()
    url = models.CharField(max_length=256, null=True, blank=True)
    receiver = models.ManyToManyField(User)




