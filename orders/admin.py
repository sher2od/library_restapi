from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'issued_by', 'status', 'borrow_date', 'due_date', 'reserved_until')
    list_filter = ('status',)
    search_fields = ('client__username',)
    inlines = [OrderItemInline]
