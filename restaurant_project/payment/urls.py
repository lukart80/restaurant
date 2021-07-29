from django.urls import path
from . import views

urlpatterns = [
    path('del/<int:order_id>/', views.make_payment_for_delivery,
         name='pay_for_delivery'),
    path('success/', views.PaymentSuccess.as_view(), name='payment_success'),
    path('fail/', views.PaymentFail.as_view(), name='payment_fail'),
    path('pickup/<int:order_id>/', views.make_payment_for_pickup, name='pay_for_pickup')
]
