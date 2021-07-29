from django.shortcuts import redirect


def payment_handler(payment_form, order_obj):
    cd = payment_form.cleaned_data
    cvv = cd['cvv']
    if cvv == '123':
        for product in order_obj.products.all():
            product.product.quantity -= product.quantity
            product.save()
            product.product.save()
        order_obj.payed = True
        order_obj.status = 'cooking'
        order_obj.save()
        return redirect('payment_success')
    return redirect('payment_fail')