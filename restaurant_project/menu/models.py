from django.core.validators import MinValueValidator, MaxLengthValidator
from django.db import models


class Cuisine(models.Model):
    """Модель для названий кухнь."""
    name = models.CharField(verbose_name='кухня', max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель названий продуктов."""
    name = models.CharField(verbose_name='Название продукта', max_length=100)
    price = models.DecimalField(
        verbose_name='Цена продукта',
        validators=[MinValueValidator(0)],
        decimal_places=2,
        max_digits=30000,
    )
    quantity = models.PositiveIntegerField(verbose_name='количество')
    cuisine = models.ForeignKey(Cuisine,
                                on_delete=models.CASCADE,
                                related_name='products',
                                verbose_name='кухня')
    picture = models.URLField(verbose_name='картинка')
    description = models.TextField(validators=[MaxLengthValidator(3000)],
                                   verbose_name='описание')

    def __str__(self):
        return self.name
