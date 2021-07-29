from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView
from order.models import DeliveryOrder, PickUpOrder
from .forms import PaymentForm
from .utils import payment_handler


def make_payment_for_delivery(request, order_id):
    order = get_object_or_404(DeliveryOrder, pk=order_id)
    if order.status != 'unpaid':
        return HttpResponseForbidden()
    form = PaymentForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            return payment_handler(form, order)
        return render(request, 'payment/make_payment.html', context)

    return render(request, 'payment/make_payment.html', context)


class PaymentSuccess(TemplateView):
    template_name = 'payment/payment_success.html'


class PaymentFail(TemplateView):
    template_name = 'payment/payment_fail.html'


def make_payment_for_pickup(request, order_id):
    order = get_object_or_404(PickUpOrder, pk=order_id)
    if order.status != 'unpaid':
        return HttpResponseForbidden()
    form = PaymentForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            return payment_handler(form, order)
        return render(request, 'payment/make_payment.html', context)

    return render(request, 'payment/make_payment.html', context)