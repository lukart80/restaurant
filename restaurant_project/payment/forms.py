from django import forms


class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, min_length=16, label='Номер карты')
    cvv = forms.CharField(max_length=3, min_length=3)
