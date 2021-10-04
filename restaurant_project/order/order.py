import random

from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import OrderItem, PickUpOrder, DeliveryOrder


class BaseOrderHandler:
    def __init__(self, request):
        self.session = request.session
        self.orders_ids = []
        self.order_model = None

    def add_order_to_session(self, order_id):
        """Добавляет заказы в сессию."""
        self.orders_ids.append(order_id)

    def return_orders(self):
        """Возвращает все доступные заказы из определенной модели"""
        if self.orders_ids:
            orders = []
            for order_id in self.orders_ids:
                order = get_object_or_404(self.order_model, pk=str(order_id))
                orders.append(order)
            return reversed(orders)
        return None


class PickUpOrderHandler(BaseOrderHandler):
    def __init__(self, request):
        super().__init__(request)
        self.orders_ids = self.session.setdefault(
            settings.PICKUP_ORDERS_KEY,
            [])
        self.order_model = PickUpOrder


class DeliveryOrderHandler(BaseOrderHandler):
    def __init__(self, request):
        super().__init__(request)
        self.orders_ids = self.session.setdefault(
            settings.DELIVERY_ORDERS_KEY,
            [])
        self.order_model = DeliveryOrder


class OrderProcessor:
    """Класс для работы с заказом."""

    def __init__(self, request, form, cart, handler):
        self.session = request.session

        self.handler = handler
        self.cart = cart
        self.form = form

    def process_order(self):
        """Метод добавляет заказ в БД и в сессию."""
        order = self.form.save(commit=False)
        order.session_id = self.session.session_key
        order.price = self.cart.get_total_price
        order.code = random.randint(100, 999)
        order.save()
        for item in self.cart:
            product = item['product']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity']
            )
        self.cart.delete_cart()
        self.handler.add_order_to_session(order.pk)
        return order

    def show_order(self):
        return self.handler.return_orders()
