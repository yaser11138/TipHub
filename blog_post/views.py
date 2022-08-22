from django.shortcuts import render , get_object_or_404
from .models import Post


def post_detail(request, post_id):
    post = get_object_or_404(klass=Post, id=post_id)
    return render(request, "video-detail.html", context={"post": post})
