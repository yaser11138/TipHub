from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Post
from .forms import PostForm
from accounts.decorators import teacher_login_required


def post_detail(request, post_id):
    post = get_object_or_404(klass=Post, id=post_id)
    context = {
        "post": post,
    }
    return render(request, "blog/video-detail.html", context=context)


def post_like(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(klass=Post, id=post_id)
        if request.user not in post.likes.all():
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)
    else:
        messages.add_message(request, messages.ERROR, "برای لایک کردن ابتدا وارد حساب کاربری خود شوید")
    return redirect(reverse("post-detail", args=[post_id]))


@teacher_login_required
def post_create(request):
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse("teacher-panel"))
        else:
            return render(request, "blog/create-post.html", context={"form": post_form})
    else:
        post_form = PostForm()
        return render(request, "blog/create-post.html", context={"form": post_form})


@teacher_login_required
def perview_post(request, post_id):
    post = get_object_or_404(klass=Post, id=post_id, user=request.user)
    context = {
        "post": post,
    }
    return render(request, "blog/video-detail.html", context=context)


@teacher_login_required
def post_delete(request, post_id):
    post = get_object_or_404(klass=Post,id=post_id, author=request.user)
    post.delete()
    return redirect(reverse("teacher-panel"))


@teacher_login_required
def post_edit(request, post_id):
    post = get_object_or_404(klass=Post, id=post_id, author=request.user)
    if request.method == "POST":
        post_form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if post_form.is_valid():
            post_form.save()
            return render(request, "blog/edit-post.html", context={"form": post_form})
        else:
            return render(request, "blog/edit-post.html", context={"form": post_form})
    else:
        post_form = PostForm(instance=post)
        return render(request, "blog/edit-post.html", context={"form": post_form})


@teacher_login_required
def post_delete(request, post_id):
    post = get_object_or_404(klass=Post, id=post_id, author=request.user)
    post.delete()
    return redirect(reverse("teacher-panel"))
