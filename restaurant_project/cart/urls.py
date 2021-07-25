from django.urls import path
from . import views

urlpatterns = [
    path('<int:product_id>/add/', views.add_product_view, name='add_to_cart'),
    path('<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('show/', views.show_cart, name='show_cart')
]
