import random
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DeliveryOrderForm, PickUpOrderForm
from django.core import serializers
from cart.cart import Cart
from menu.models import Product
from .models import OrderItem, DeliveryOrder, PickUpOrder


def create_delivery_order(request):
    """View-функция для создания заказа."""
    form = DeliveryOrderForm(request.POST or None)
    if request.method == 'POST':
        cart = Cart(request)
        if not cart.cart:
            return redirect('home')

        if form.is_valid():
            order = form.save(commit=False)
            order.code = random.randint(100, 999)
            order.price = cart.get_total_price
            order.save()
            for item in cart:
                product = item['product']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity']
                )
            cart.delete_cart()
            customer_orders = request.session.setdefault('orders_delivery', [])
            customer_orders.append(str(order.pk))

            return redirect('home')
        context = {'form': form}
        return render(request, 'order/create_order.html', context)
    context = {'form': form}
    return render(request, 'order/create_order.html', context)


def show_orders(request):
    delivery_orders_ids = request.session.get('orders_delivery')
    if delivery_orders_ids:
        delivery_orders = []
        for str_order_id in delivery_orders_ids:
            order_del = get_object_or_404(DeliveryOrder, pk=int(str_order_id))
            delivery_orders.append(order_del)
    else:
        delivery_orders = None
    context = {
        'delivery_orders': delivery_orders
    }
    return render(request, 'order/show_orders.html', context)
