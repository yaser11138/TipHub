from django.urls import path
from . import views


urlpatterns = [
    path("post/<int:post_id>/", views.post_detail, name="post-detail"),
    path("post/<int:post_id>/comment/add/", views.add_comment, name="add-comment"),
    path("post/<int:post_id>/<int:parent_comment_id>/reply/add/", views.add_comment, name="add-reply"),
]
