from django.db import models

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
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    code = models.IntegerField()
    payed = models.BooleanField(default=False)

    class Meta:
        abstract = True


class DeliveryOrder(BaseOrder):
    status = models.CharField(choices=STATUS_CHOICES_DELIVERY)
    delivery_address = models.CharField(max_length=100)


class PickUpOrder(BaseOrder):
    status = models.CharField(choices=STATUS_CHOICES_PICKUP)
    restaurant = models.CharField(choices=RESTAURANT_CHOICES)
