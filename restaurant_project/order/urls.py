from django.urls import path
from . import views
urlpatterns = (
    path('create_delivery/', views.create_delivery_order, name='create_delivery'),
    path('show/', views.show_orders, name='show_orders'),
    path('create_pickup/', views.create_pick_up_order, name='create_pickup'),
)
