from django.shortcuts import render
from blog.models import Category


def homepage(request):
    return render(request, "index.html")