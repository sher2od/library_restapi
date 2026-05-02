from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'status', 'payment_type', 'created_at')
    list_filter = ('status', 'payment_type')
    search_fields = ('order__client__username', 'order__id')
