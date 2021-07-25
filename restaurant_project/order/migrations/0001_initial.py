# Generated by Django 3.2.5 on 2021-07-25 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('menu', '0003_auto_20210725_2150'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('code', models.IntegerField()),
                ('payed', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('unpaid', 'неоплачен'), ('cooking', 'готовится'), ('delivering', 'доставляется'), ('received', 'получен')], max_length=100)),
                ('delivery_address', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PickUpOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('code', models.IntegerField()),
                ('payed', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('unpaid', 'неоплачен'), ('cooking', 'готовится'), ('ready', 'готов'), ('received', 'получен')], max_length=100)),
                ('restaurant', models.CharField(choices=[('loc1', 'Первый ресторан'), ('loc2', 'Второй ресторан'), ('loc3', 'Третий ресторан')], max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(limit_choices_to={'model__in': ('PickUpOrder', 'DeliveryOrder')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='menu.product')),
            ],
        ),
    ]
