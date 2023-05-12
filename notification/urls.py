from django.urls import path
from .views import notifications_handel

urlpatterns = [
    path("<notification_id>/", notifications_handel, name="notification"),

]