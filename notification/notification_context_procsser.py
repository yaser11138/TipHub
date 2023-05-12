from .models import Notification


def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(receiver__in=[request.user])
    else:
        notifications = None
    return {"notifications": notifications}

