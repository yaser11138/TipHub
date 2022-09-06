from django.contrib import admin
from .models import Post, Category
from .forms import CategoryForm


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    form = CategoryForm
