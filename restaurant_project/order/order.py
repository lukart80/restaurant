from abc import ABC, abstractmethod
import random

from django.conf import settings
from django.shortcuts import get_object_or_404

from .forms import PickUpOrderForm
from cart.cart import Cart

from .models import OrderItem, PickUpOrder


class BaseOrderProcessor(ABC):
    """Базовый класс для заказа"""

    def __init__(self, request):
        self.session = request.session

    @abstractmethod
    def add_order_to_db(self, form, cart):
        raise NotImplementedError

    @abstractmethod
    def show_all_orders(self):
        raise NotImplementedError

    @abstractmethod
    def add_order_to_session(self, order_id):
        raise NotImplementedError


class PickUpOrderProcessor(BaseOrderProcessor):
    """Класс для работы с заказами самовывоза."""
    def __init__(self, request):
        super().__init__(request)
        self.orders_ids = self.session.setdefault(
            settings.PICKUP_ORDERS_KEY,
            [])

    def add_order_to_db(self, form: PickUpOrderForm, cart: Cart):
        """Метод добавляет заказ в БД."""
        order = form.save(commit=False)
        order.session_id = self.session.session_key
        order.price = cart.get_total_price
        order.code = random.randint(100, 999)
        order.save()
        for item in cart:
            product = item['product']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity']
            )
        cart.delete_cart()
        return order

    def show_all_orders(self):
        """Метод возвращает список всех заказов самовывозом."""
        if self.orders_ids:
            orders = []
            for order_id in self.orders_ids:
                order = get_object_or_404(PickUpOrder, pk=str(order_id))
                orders.append(order)
            return reversed(orders)
        return None

    def add_order_to_session(self, order_id):
        """Метод добавляет в сессию id заказа."""
        self.orders_ids.append(order_id)



