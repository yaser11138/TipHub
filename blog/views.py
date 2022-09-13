import hitcount.views
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
from accounts.decorators import teacher_login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from jdatetime import date
from .models import Post, Category
from .forms import PostForm


def post_detail(request, year, month, day, slug):
    publish_date = date(year=year, month=month, day=day).strftime("%Y-%m-%d")
    post = get_object_or_404(klass=Post, slug=slug, publish=publish_date)
    context = {
        "post": post,
    }
    return render(request, "blog/video-detail.html", context=context)


def posts(request, category_slug=None):
    posts = Post.published.all()
    category = None

    if category_slug:
        category = get_object_or_404(klass=Category, slug=category_slug)
        posts = posts.filter(category=category)
    if request.GET.get("tag"):
        posts = posts.filter(tags__slug__in=[request.GET.get("tag")])
    if request.GET.get("sort"):
        posts = posts.order_by(request.GET.get("sort"))
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(posts, 12)
    pages = paginator.get_elided_page_range(page_number, on_each_side=1)
    current_page = paginator.get_page(page_number)
    context = {
        "posts": posts,
        "category": category,
        "pages": pages,
        "current_page": current_page,
    }
    return render(request, "blog/all-videos.html", context=context)


def post_like(request, post_id):
    post = get_object_or_404(klass=Post, id=post_id)
    if request.user.is_authenticated:
        if request.user not in post.likes.all():
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)
    else:
        messages.add_message(request, messages.ERROR, "برای لایک کردن ابتدا وارد حساب کاربری خود شوید")
    return redirect(post.get_absolute_url())


def search(request):
    q = request.GET.get("q", None)
    if q:
        vector = SearchVector('title', weight='A') + SearchVector("tags__name", weight='B') +\
                 SearchVector("body", weight='C')
        query = SearchQuery(q)
        posts = Post.objects.annotate(rank=SearchRank(vector, query, cover_density=True)).order_by("-rank")
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(posts, 12)
    pages = paginator.get_elided_page_range(page_number, on_each_side=1)
    current_page = paginator.get_page(page_number)
    context = {
        "posts": posts,
        "pages": pages,
        "current_page": current_page,
    }
    return render(request, "blog/all-videos.html", context=context)


@teacher_login_required
def post_create(request):
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        print(post_form)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            post_form.save_m2m()
            return redirect(reverse("teacher-panel"))
        else:
            return render(request, "blog/create-post.html", context={"form": post_form})
    else:
        post_form = PostForm()
        return render(request, "blog/create-post.html", context={"form": post_form})


@teacher_login_required
def perview_post(request, post_id):
    post = get_object_or_404(klass=Post, id=post_id, author=request.user)
    context = {
        "post": post,
    }
    return render(request, "blog/video-detail.html", context=context)


@teacher_login_required
def post_delete(request, post_id):
    post = get_object_or_404(klass=Post, id=post_id, author=request.user)
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
            print(post_form.errors)
            return render(request, "blog/edit-post.html", context={"form": post_form})
    else:
        post_form = PostForm(instance=post)
        return render(request, "blog/edit-post.html", context={"form": post_form})

