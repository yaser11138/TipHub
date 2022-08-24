from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.messages import add_message
from .models import Post


def post_detail(request, post_id):
    post = get_object_or_404(klass=Post, id=post_id)
    context = {
        "post": post,
    }
    return render(request, "video-detail.html", context=context)
