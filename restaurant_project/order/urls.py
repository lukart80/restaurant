from django.urls import path
from . import views
urlpatterns = (
    path('create_delivery/', views.create_delivery_order, name='create_delivery'),
    path('show/', views.show_orders, name='show_orders')
)
