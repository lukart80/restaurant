from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from menu.models import Product
from .services import check_quantity


def add_product_view(request, product_id):
    """View функция для добавление продукта в корзину."""

    product = get_object_or_404(Product, id=product_id)
    try:
        check_quantity(product, 1)
    except ValueError:
        return redirect('home')
    cart = Cart(request)
    cart.add_item(product)
    return redirect('home')


def show_cart(request):
    """View-функция для простомтра корзины."""
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'cart/cart_show.html', context)


def delete_product(request, product_id):
    """View-функция для удаления продукта"""
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.delete_product(product)
    return redirect('home')
