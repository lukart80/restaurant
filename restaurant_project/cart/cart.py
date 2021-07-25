from decimal import Decimal

from django.conf import settings

from menu.models import Product


class Cart:
    """Представление корзины в виде класса"""

    def __init__(self, request):
        self.session = request.session
        self.cart = request.session.setdefault(settings.CART_ID, {})

    def save(self):
        self.session.modified = True

    def add_item(self, product: Product, quantity=1):
        """Метод для добавление продукта."""
        product_id = str(product.pk)
        if product_id in self.cart.keys():
            self.cart[product_id]['quantity'] += quantity

        else:
            self.cart[product_id] = {'quantity': quantity,
                                     'price': str(product.price),
                                     }

        self.save()

    def override_quantity(self, product_id, quantity):
        """Метод установки количества товара."""
        self.cart[product_id]['quantity'] = quantity

    def delete_product(self, product):
        """Метод для удаление товара."""
        del self.cart[str(product.id)]
        self.save()

    def delete_cart(self):
        """Метод для удаления корзины."""
        del self.cart

    def get_product_price(self, product_id):
        """Метод для подсчета стоимости одного товара."""
        return self.cart[product_id]['price'] * self.cart[product_id][
            'quantity']

    @property
    def get_total_price(self):
        """Метод для подсчета стоимости всех товаров."""
        return sum(
            Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """Итератор возвращает данные товаров в корзине."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.pk)]['product'] = product
            round(Decimal(cart[str(product.pk)]['price']))

        for item in cart.values():
            yield item

    def count_products_in_cart(self):
        """Метод для подсчета товаров в корзине."""
        return len(self.cart.keys())
