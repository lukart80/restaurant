from decimal import Decimal

from django.test import TestCase, Client
from django.urls import reverse

from menu.models import Cuisine, Product


class TestMenuViews(TestCase):
    # Texts
    CUISINE_NAME = 'cuisine'
    PRODUCT_NAME = 'product name'
    PRODUCT_PRICE = round(Decimal(23.32), 2)
    PRODUCT_QUANTITY = 10
    PRODUCT_PICTURE = 'www.yandex.ru'
    PRODUCT_DESCRIPTION = 'тест описание продукта'

    # URLs names
    HOMEPAGE_NAME = 'home'

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

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cuisine = Cuisine.objects.create(
            name=cls.CUISINE_NAME
        )
        cls.product = Product.objects.create(
            name=cls.PRODUCT_NAME,
            price=cls.PRODUCT_PRICE,
            quantity=cls.PRODUCT_QUANTITY,
            cuisine=cls.cuisine,
            picture=cls.PRODUCT_PICTURE,
            description=cls.PRODUCT_DESCRIPTION,

        )

    def setUp(self):
        self.anonymous_client = Client()

    def test_correct_templates_used_by_name(self):
        """Проверяем, что используются нужные шаблоны при обращении по
        имени. """
        name_template = {
            self.HOMEPAGE_NAME: self.HOMEPAGE_TEMPLATE
        }
        for name, template in name_template.items():
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertTemplateUsed(response, template)

    def test_homepage_contains_product(self):
        """Проверяем корректное отображение продукта на домашней странице."""
        attribute_expected = {
            self.NAME_ATTR: self.PRODUCT_NAME,
            self.PRICE_ATTR: self.PRODUCT_PRICE,
            self.QUANTITY_ATTR: self.PRODUCT_QUANTITY,
            self.CUISINE_ATTR: self.__class__.cuisine,
            self.DESCRIPTION_ATTR: self.PRODUCT_DESCRIPTION,
            self.PICTURE_ATTR: self.PRODUCT_PICTURE
        }
        response = self.client.get(reverse('home'))
        product_object = response.context[self.PAGE_VAR][0]
        for attribute, expected in attribute_expected.items():
            with self.subTest(attribute=attribute):
                self.assertEqual(
                    getattr(product_object, attribute),
                    expected
                )


class TestMenuPaginator(TestCase):
    # Texts
    CUISINE_NAME = 'cuisine'
    PRODUCT_NAME = 'product name'
    PRODUCT_PRICE = round(Decimal(23.32), 2)
    PRODUCT_QUANTITY = 10
    PRODUCT_PICTURE = 'www.yandex.ru'
    PRODUCT_DESCRIPTION = 'тест описание продукта'

    # URLs names
    HOMEPAGE_NAME = 'home'
    SECOND_PAGE = '?page=2'

    # Context vars
    PAGE_VAR = 'page'

    def setUp(self):
        self.client = Client()
        self.cuisine = Cuisine.objects.create(
            name=self.CUISINE_NAME
        )
        obj = list(
            Product(
                name=self.PRODUCT_NAME,
                price=self.PRODUCT_PRICE,
                quantity=self.PRODUCT_QUANTITY,
                cuisine=self.cuisine,
                picture=self.PRODUCT_PICTURE,
                description=self.PRODUCT_DESCRIPTION,
            ) for _ in range(11)
        )
        Product.objects.bulk_create(obj)

    def test_paginator_pages(self):
        """Проверка страниц с паджинатором."""
        url_value = {
            reverse(self.HOMEPAGE_NAME): 9,
            reverse(self.HOMEPAGE_NAME) + self.SECOND_PAGE: 2
        }
        for url, value in url_value.items():
            response = self.client.get(url)
            with self.subTest(url=url):
                page_obj = response.context[self.PAGE_VAR]
                self.assertEqual(len(page_obj), value)
