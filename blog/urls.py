from django.urls import path
from django_comments_xtd import urls
from . import views

urlpatterns = [
    path("post/<int:post_id>/", views.post_detail, name="post-detail"),
]
