from django.conf import settings


class Cart:
    """Представление корзины в виде класса"""

    def __init__(self, request):
        self.session = request.session
        self.cart = request.session.setdefault(settings.CART_ID, {})

    def save(self):
        self.session.modified = True

    def add_item(self, product_id, product_price, quantity=1):
        """Метод для добавление продукта."""
        if product_id in self.cart.keys():
            self.cart[product_id]['quantity'] += quantity
            return None
        self.cart[product_id] = {}
        self.cart[product_id]['quantity'] = quantity
        self.cart[product_id]['price'] = product_price
        self.cart.save()

    def override_quantity(self, product_id, quantity):
        """Метод установки количества товара."""
        self.cart[product_id]['quantity'] = quantity

    def delete_product(self, product_id):
        """Метод для удаление товара."""
        del self.cart[product_id]

    def delete_cart(self):
        """Метод для удаления корзины."""
        del self.cart

    def get_product_price(self, product_id):
        """Метод для подсчета стоимости одного товара."""
        return self.cart[product_id]['price'] * self.cart[product_id]['quantity']

    def get_total_price(self):
        """Метод для подсчета стоимости всех товаров."""
        return sum(item['price'] * item['quantity'] for item in self.cart.values())
