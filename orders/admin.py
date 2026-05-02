from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'copy', 'client', 'issued_by', 'status', 'borrow_date', 'due_date')
    list_filter = ('status',)
    search_fields = ('client__username', 'copy__barcode', 'copy__book__title')
