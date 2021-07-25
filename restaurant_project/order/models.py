from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from menu.models import Product

STATUS_CHOICES_DELIVERY = [
    ('unpaid', 'неоплачен'),
    ('cooking', 'готовится'),
    ('delivering', 'доставляется'),
    ('received', 'получен'),
]

STATUS_CHOICES_PICKUP = [
    ('unpaid', 'неоплачен'),
    ('cooking', 'готовится'),
    ('ready', 'готов'),
    ('received', 'получен'),
]

RESTAURANT_CHOICES = [
    ('loc1', 'Первый ресторан'),
    ('loc2', 'Второй ресторан'),
    ('loc3', 'Третий ресторан'),
]


class BaseOrder(models.Model):
    """Базовая модель заказа."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    code = models.IntegerField()
    payed = models.BooleanField(default=False)
    products = GenericRelation('OrderItem',
                               content_type_field='content_type',
                               object_id_field='object_id'
                               )

    class Meta:
        abstract = True


class DeliveryOrder(BaseOrder):
    """Модель для заказа с доствкой."""
    status = models.CharField(choices=STATUS_CHOICES_DELIVERY, max_length=100)
    delivery_address = models.CharField(max_length=100)

    def __str__(self):
        return f'Доставка номер {self.id}'


class PickUpOrder(BaseOrder):
    """Модель для заказа самовывозом."""
    status = models.CharField(choices=STATUS_CHOICES_PICKUP, max_length=100)
    restaurant = models.CharField(choices=RESTAURANT_CHOICES, max_length=100)

    def __str__(self):
        return f'Самовывоз {self.id}'


class OrderItem(models.Model):
    """Модель для хранения заказанных продуктов."""
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,

                                     )
    object_id = models.PositiveIntegerField()
    order = GenericForeignKey('content_type', 'object_id')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='orders')

    def __str__(self):
        return self.product.name
