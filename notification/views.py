from django.shortcuts import render, get_object_or_404, redirect
from .models import Notification
# Create your views here.


def notifications_handel(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    if Notification.url:
        url = notification.url
        notification.delete()
        return redirect(url)

