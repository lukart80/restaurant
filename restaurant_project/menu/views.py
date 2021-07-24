from django.shortcuts import render


def homepage_view(request):
    """View-функция для отображения главной страницы."""
    return render(request, 'menu/homepage.html', {})
