import random
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import DeliveryOrder, OrderItem


def get_user_data_from_session(request):
    """Функция возращает данный пользователя, хранящиеся в session,
    если нет, то None."""
    user_data = request.session.get(settings.USER_DATA_KEY)
    return user_data


def alter_user_data_in_session(request):
    """Функция изменяет данные пользователя на основе POST запроса."""

    request.session['user_data'] = {
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name'],
        'email': request.POST['email'],
    }


def send_order_and_items_to_db(session_id, form_obj, cart_obj):
    """Функция сохранит заказ и входящие в него продукты в базу данных,
    возвращает сохраненный заказ. """
    order = form_obj.save(commit=False)
    order.session_id = session_id
    order.code = random.randint(100, 999)
    order.price = cart_obj.get_total_price
    order.save()
    for item in cart_obj:
        product = item['product']
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity']
        )
    cart_obj.delete_cart()
    return order


def generate_order_code():
    """Функция генерирует код заказа от 100 до 999."""
    # TODO надо сделать, чтобы функция не сгенерировала существующий код
    #  заказа
    pass


def add_order_to_session(request, order_obj, key):
    """Добавляет id созданного заказа в session."""
    customer_orders = request.session.setdefault(key, [])
    customer_orders.append(str(order_obj.pk))


def get_orders_from_session(request, order_model):
    """Функция возвращает список заказов из сессии."""
    if order_model is DeliveryOrder:
        orders_ids = request.session.get(settings.DELIVERY_ORDERS_KEY)
    else:
        orders_ids = request.session.get(settings.PICKUP_ORDERS_KEY)
    if orders_ids:
        delivery_orders = []
        for str_order_id in orders_ids:
            order_del = get_object_or_404(order_model, pk=int(str_order_id))
            delivery_orders.append(order_del)
        return reversed(delivery_orders)
    return None
