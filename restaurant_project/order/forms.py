from django import forms
from .models import PickUpOrder, DeliveryOrder


class PickUpOrderForm(forms.ModelForm):
    class Meta:
        model = PickUpOrder
        fields = ('first_name', 'last_name', 'email', 'restaurant')
        labels = {'first_name': 'имя',
                  'last_name': 'фамилия',
                  'restaurant': 'ресторан',
                  }
        help_texts = {'email': 'Введите для связи',
                      'restaurant': 'Выберите где забрать ваш заказ'}


class DeliveryOrderForm(forms.ModelForm):
    class Meta:
        model = DeliveryOrder
        fields = ('first_name', 'last_name', 'email', 'delivery_address')
        labels = {'first_name': 'имя',
                  'last_name': 'фамилия',
                  'delivery_address': 'адрес',
                  }
        help_texts = {'email': 'Введите для связи',
                      'delivery_address': 'Куда доставить заказ'}
