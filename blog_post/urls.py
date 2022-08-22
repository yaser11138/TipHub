from django.urls import path
from .views import post_detail

urlpatterns = [
    path("post/<int:post_id>/", post_detail, name="post-detail"),
]