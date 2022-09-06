from .models import Category


def category_processor(request):
    category = Category.objects.all()
    return {"categories": category}