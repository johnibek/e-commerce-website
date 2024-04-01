from .models import Category

def category(request):
    categories = Category.objects.all()
    return {'categories': categories}
