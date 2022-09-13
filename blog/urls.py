from django.urls import path
from django_comments_xtd import urls
from . import views

urlpatterns = [
    path("post/<int:year>/<int:month>/<int:day>/<str:slug>/", views.post_detail, name="post-detail"),
    path("post/<int:post_id>/like", views.post_like, name="post-like"),
    path("post/create/", views.post_create, name="post-create"),
    path("post/preview/<int:post_id>/", views.perview_post, name="post-preview"),
    path("post/edit/<int:post_id>/", views.post_edit, name="post-edit"),
    path("post/delete/<int:post_id>/", views.post_delete, name="post-delete"),
    path("post/all/", views.posts, name="all-posts"),
    path("post/category/<slug:category_slug>/", views.posts, name="posts-filter-by-category"),
    path("post/search/", views.search, name="post-search"),
]
