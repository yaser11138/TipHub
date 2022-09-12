from django.shortcuts import render
from blog.models import Category, Post


def homepage(request):
    try:
        new_posts = Post.objects.order_by("-publish")[:5]
        popular_posts = Post.objects.order_by("-hit_count_generic__hits")[:5]
    except:
        new_posts = Post.objects.order_by("-publish")
        popular_posts = Post.objects.order_by("-hit_count_generic__hits")
    context = {
        "new_posts": new_posts,
        "popular_posts": popular_posts,
    }
    return render(request, "index.html", context=context)
