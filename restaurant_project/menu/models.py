from django.core.validators import MinValueValidator, MaxLengthValidator
from django.db import models


class Cuisine(models.Model):
    cuisine = models.CharField(verbose_name='кухня', max_length=100)


class Product(models.Model):
    name = models.CharField(verbose_name='Название продукта', max_length=100)
    price = models.DecimalField(
        verbose_name='Цена продукта',
        validators=[MinValueValidator(0)],
        decimal_places=2,
        max_digits=30000,
    )
    quantity = models.PositiveIntegerField()
    cuisine = models.ForeignKey(Cuisine,
                                on_delete=models.CASCADE,
                                related_name='products')
    picture = models.URLField()
    description = models.TextField(validators=[MaxLengthValidator(3000)])
