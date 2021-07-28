from cart.cart import Cart
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import DeliveryOrderForm, PickUpOrderForm
from .utils import (get_user_data_from_session, alter_user_data_in_session,
                    send_order_and_items_to_db, add_order_to_session,
                    get_orders_from_session)
from .models import DeliveryOrder, PickUpOrder

def create_delivery_order(request):
    """View-функция для создания заказа."""
    session_id = request.session.session_key
    user_data = get_user_data_from_session(request)
    form = DeliveryOrderForm(initial=user_data)
    if request.method == 'POST':
        form = DeliveryOrderForm(data=request.POST)
        cart = Cart(request)
        if not cart.cart:
            return redirect('home')

        if form.is_valid():
            order = send_order_and_items_to_db(session_id, form, cart)
            add_order_to_session(request, order, settings.DELIVERY_ORDERS_KEY)
            alter_user_data_in_session(request)

            return redirect('show_orders')
        context = {'form': form}
        return render(request, 'order/create_order.html', context)
    context = {'form': form}
    return render(request, 'order/create_order.html', context)


def show_orders(request):
    """View-функция для просмотра всех заказов."""
    delivery_orders = get_orders_from_session(request, DeliveryOrder)
    pickup_orders = get_orders_from_session(request, PickUpOrder)
    context = {
        'delivery_orders': delivery_orders,
        'pickup_orders': pickup_orders,
    }
    return render(request, 'order/show_orders.html', context)


def create_pick_up_order(request):
    session_id = request.session.session_key
    user_data = get_user_data_from_session(request)
    form = PickUpOrderForm(initial=user_data)
    if request.method == 'POST':
        form = PickUpOrderForm(request.POST)
        cart = Cart(request)
        if form.is_valid():
            order = send_order_and_items_to_db(session_id, form, cart)
            add_order_to_session(request, order, settings.PICKUP_ORDERS_KEY)
            alter_user_data_in_session(request)
            return redirect('show_orders')
        context = {'form': form}
        return render(request, 'order/create_order.html', context)
    context = {'form': form}
    return render(request, 'order/create_order.html', context)
