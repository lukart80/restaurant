from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import DeliveryOrder, PickUpOrder, OrderItem


class OrderItemInline(GenericTabularInline):
    model = OrderItem
    extra = 1


@admin.register(DeliveryOrder)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'status', 'price')
    list_filter = ('price',)
    search_fields = ('last_name', 'status',)
    inlines = [OrderItemInline, ]


@admin.register(PickUpOrder)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'status', 'price')
    list_filter = ('price',)
    search_fields = ('last_name', 'status',)
    inlines = [OrderItemInline, ]
