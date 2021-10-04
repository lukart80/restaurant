from decimal import Decimal

from django.test import TestCase, Client
from django.shortcuts import reverse
from menu.models import Cuisine, Product
from ..models import PickUpOrder, DeliveryOrder


class TestOrderView(TestCase):
    # Texts
    CUISINE_NAME = 'cuisine'
    PRODUCT_NAME = 'product name'
    PRODUCT_PRICE = round(Decimal(23.32), 2)
    PRODUCT_QUANTITY = 10
    PRODUCT_PICTURE = 'www.yandex.ru'
    PRODUCT_DESCRIPTION = 'тест описание продукта'

    # Urls names
    CREATE_DELIVERY = 'create_delivery'
    SHOW = 'show_orders'
    CREATE_PICKUP = 'create_pickup'
    ADD_TO_CART = 'add_to_cart'

    # Templates
    HOMEPAGE_TEMPLATE = 'menu/homepage.html'

    # Attributes
    NAME_ATTR = 'name'
    PRICE_ATTR = 'price'
    QUANTITY_ATTR = 'quantity'
    PICTURE_ATTR = 'picture'
    DESCRIPTION_ATTR = 'description'
    CUISINE_ATTR = 'cuisine'

    # Context vars
    PAGE_VAR = 'page'
    # Client info
    CLIENT_NAME = 'tester'
    CLIENT_SURNAME = 'tester'
    RESTAURANT = 'loc1'
    EMAIL = 'test@test.com'

    def setUp(self):
        self.anonymous_client1 = Client()
        self.anonymous_client2 = Client()

        self.cuisine = Cuisine.objects.create(
            name=self.CUISINE_NAME
        )
        self.product1 = Product.objects.create(
            name=self.PRODUCT_NAME,
            price=self.PRODUCT_PRICE,
            quantity=self.PRODUCT_QUANTITY,
            cuisine=self.cuisine,
            picture=self.PRODUCT_PICTURE,
            description=self.PRODUCT_DESCRIPTION,

        )
        self.product2 = Product.objects.create(
            name=self.PRODUCT_NAME,
            price=self.PRODUCT_PRICE,
            quantity=self.PRODUCT_QUANTITY,
            cuisine=self.cuisine,
            picture=self.PRODUCT_PICTURE,
            description=self.PRODUCT_DESCRIPTION,

        )
        self.product1_id = self.product1.pk
        self.product2_id = self.product2.pk

    def test_create_pickup_order(self):
        """Проверяем создание заказа самовывозом."""
        form_data = {
            'first_name': self.CLIENT_NAME,
            'last_name': self.CLIENT_SURNAME,
            'email': self.EMAIL,
            'restaurant': self.RESTAURANT
        }
        self.anonymous_client1.get(reverse(self.ADD_TO_CART, args=[self.product1_id]))
        response = self.anonymous_client1.post(
            reverse(self.CREATE_PICKUP), data=form_data, follow=True
        )
        self.assertRedirects(response, reverse(self.SHOW))

        created_order = PickUpOrder.objects.first()
        attribute_expected = {
            created_order.first_name: self.CLIENT_NAME,
            created_order.last_name: self.CLIENT_SURNAME,
            created_order.email: self.EMAIL,
            created_order.restaurant: self.RESTAURANT
        }

        for attribute, expected in attribute_expected.items():
            with self.subTest(attribute=attribute):
                self.assertEqual(attribute, expected)





