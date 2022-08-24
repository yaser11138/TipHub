from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.messages import add_message
from .models import Post, Comment
from .forms import CommentAddForm


def post_detail(request, post_id):
    post = get_object_or_404(klass=Post, id=post_id)
    comments = post.comments.filter(post=post, active=True, parent=None)
    context = {
        "post": post,
        "comments": comments,
    }
    return render(request, "video-detail.html", context=context)


@require_POST
@login_required()
def add_comment(request, post_id, parent_comment_id=None):
    post = get_object_or_404(klass=Post, id=post_id)
    comment = CommentAddForm(request.POST)
    if comment.is_valid():
        comment = comment.save(commit=False)
        comment.author = request.user
        comment.post = post
        if parent_comment_id:
            parent_comment = get_object_or_404(klass=Comment, id=parent_comment_id)
            comment.parent = parent_comment
        comment.save()
        return redirect(reverse("post-detail", args=[post_id]))
    else:
        messages.add_message(request, level=messages.ERROR, message=comment.errors)
        return redirect(reverse("post-detail", args=[post_id]))
