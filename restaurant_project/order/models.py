from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
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
    session_id = models.CharField(default=0, max_length=150)
    first_name = models.CharField(max_length=50, verbose_name='имя')
    last_name = models.CharField(max_length=50, verbose_name='фамилия')
    email = models.EmailField()
    code = models.IntegerField(verbose_name='код')
    payed = models.BooleanField(default=False, verbose_name='оплачено')
    products = GenericRelation('OrderItem',
                               content_type_field='content_type',
                               object_id_field='object_id',

                               )
    price = models.PositiveIntegerField(default=0, verbose_name='цена')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-date']


class DeliveryOrder(BaseOrder):
    """Модель для заказа с доствкой."""
    status = models.CharField(choices=STATUS_CHOICES_DELIVERY,
                              max_length=100,
                              verbose_name='статус',
                              default='unpaid')
    delivery_address = models.CharField(max_length=100,
                                        verbose_name='адрес доставки')

    def __str__(self):
        return f'Доставка номер {self.id}'


class PickUpOrder(BaseOrder):
    """Модель для заказа самовывозом."""
    status = models.CharField(choices=STATUS_CHOICES_PICKUP,
                              max_length=100,
                              verbose_name='статус',
                              default='unpaid')
    restaurant = models.CharField(choices=RESTAURANT_CHOICES,
                                  max_length=100,
                                  verbose_name='ресторан')

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
                                related_name='orders',
                                verbose_name='продукт')
    quantity = models.PositiveIntegerField(default=0,
                                           verbose_name='количество')

    def __str__(self):
        return self.product.name


@receiver(pre_delete, sender=DeliveryOrder)
@receiver(pre_delete, sender=PickUpOrder)
def remove_deleted_order_from_session(sender, instance, *args, **kwargs):
    """Функция при удалении заказа из БД удаляет его id и из сессии."""
    session = SessionStore(session_key=instance.session_id)
    if sender is DeliveryOrder:
        orders_id = session[settings.DELIVERY_ORDERS_KEY]
    else:
        orders_id = session[settings.PICKUP_ORDERS_KEY]
    orders_id.remove(str(instance.id))
    for order_id in orders_id:
        if order_id == str(instance.id):
            del order_id
    session.save()
