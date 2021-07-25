from django.contrib import admin
from .models import DeliveryOrder, PickUpOrder, OrderItem

admin.site.register(DeliveryOrder)
admin.site.register(PickUpOrder)


@admin.register(OrderItem)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('order',)




