# Generated by Django 3.2.5 on 2021-07-25 18:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_rename_cuisine_cuisine_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cuisine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='menu.cuisine', verbose_name='кухня'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(validators=[django.core.validators.MaxLengthValidator(3000)], verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='product',
            name='picture',
            field=models.URLField(verbose_name='картинка'),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(verbose_name='количество'),
        ),
    ]
