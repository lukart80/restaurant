# Generated by Django 3.2.5 on 2021-07-28 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_auto_20210726_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryorder',
            name='session_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pickuporder',
            name='session_id',
            field=models.IntegerField(default=0),
        ),
    ]
