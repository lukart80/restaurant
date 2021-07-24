from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator


def homepage_view(request):
    """View-функция для отображения главной страницы."""
    products = Product.objects.prefetch_related('cuisine').all()
    paginator = Paginator(products, 9)
    page = paginator.get_page(request.GET.get('page'))
    context = {
        'page': page,
    }
    return render(request, 'menu/homepage.html', context)
