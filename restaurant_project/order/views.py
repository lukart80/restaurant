from cart.cart import Cart
from django.shortcuts import render, redirect

from .forms import DeliveryOrderForm, PickUpOrderForm
from .utils import get_user_data_from_session, alter_user_data_in_session

from .order import OrderProcessor, PickUpOrderHandler, DeliveryOrderHandler


def create_delivery_order(request):
    """View-функция для создания заказа."""
    user_data = get_user_data_from_session(request)
    form = DeliveryOrderForm(initial=user_data)
    if request.method == 'POST':
        form = DeliveryOrderForm(request.POST)
        cart = Cart(request)
        if not cart.cart:
            return redirect('home')
        handler = DeliveryOrderHandler(request)
        order = OrderProcessor(request, form, cart, handler)

        if form.is_valid():
            order.process_order()

            alter_user_data_in_session(request)
            return redirect('show_orders')
        context = {'form': form}
        return render(request, 'order/create_order.html', context)
    context = {'form': form}
    return render(request, 'order/create_order.html', context)


def show_orders(request):
    """View-функция для просмотра всех заказов."""
    delivery_orders = DeliveryOrderHandler(request).return_orders()
    pickup_orders = PickUpOrderHandler(request).return_orders()
    context = {
        'delivery_orders': delivery_orders,
        'pickup_orders': pickup_orders,
    }
    return render(request, 'order/show_orders.html', context)


def create_pick_up_order(request):
    user_data = get_user_data_from_session(request)
    form = PickUpOrderForm(initial=user_data)
    if request.method == 'POST':
        form = PickUpOrderForm(request.POST)
        cart = Cart(request)
        if not cart.cart:
            return redirect('home')
        handler = PickUpOrderHandler(request)
        order = OrderProcessor(request, form, cart, handler)

        if form.is_valid():
            order.process_order()

            alter_user_data_in_session(request)
            return redirect('show_orders')
        context = {'form': form}
        return render(request, 'order/create_order.html', context)
    context = {'form': form}
    return render(request, 'order/create_order.html', context)
