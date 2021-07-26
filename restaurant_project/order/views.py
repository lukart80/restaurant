from cart.cart import Cart
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import DeliveryOrderForm, PickUpOrderForm
from .models import OrderItem, DeliveryOrder
from .utils import get_user_data_from_session, alter_user_data_in_session, \
    send_order_and_items_to_db, add_order_to_session


def create_delivery_order(request):
    """View-функция для создания заказа."""
    user_data = get_user_data_from_session(request)
    form = DeliveryOrderForm(initial=user_data)
    if request.method == 'POST':
        form = DeliveryOrderForm(data=request.POST)
        cart = Cart(request)
        if not cart.cart:
            return redirect('home')

        if form.is_valid():
            order = send_order_and_items_to_db(form, cart, OrderItem)
            add_order_to_session(request, order, settings.DELIVERY_ORDERS_KEY)
            alter_user_data_in_session(request)

            return redirect('show_orders')
        context = {'form': form}
        return render(request, 'order/create_order.html', context)
    context = {'form': form}
    return render(request, 'order/create_order.html', context)


def show_orders(request):

    delivery_orders_ids = request.session.get(settings.DELIVERY_ORDERS_KEY)
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


def create_pick_up_order(request):
    user_data = get_user_data_from_session(request)
    form = PickUpOrderForm(initial=user_data)
    if request.method == 'POST':
        form = PickUpOrderForm(request.POST)
        cart = Cart(request)
        if form.is_valid():
            order = send_order_and_items_to_db(form, cart, OrderItem)
            add_order_to_session(request, order, settings.PICKUP_ORDERS_KEY)
            alter_user_data_in_session(request)
            return redirect('show_orders')
        context = {'form': form}
        return render(request, 'order/create_order.html', context)
    context = {'form': form}
    return render(request, 'order/create_order.html', context)
