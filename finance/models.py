from django.db import models
from orders.models import Order
from django.conf import settings
from decimal import Decimal


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'

    class Type(models.TextChoices):
        RENTAL = 'rental', 'Rental Fee'
        FINE = 'fine', 'Overdue Fine'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_type = models.CharField(max_length=20, choices=Type.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.payment_type} for Order #{self.order.id} - {self.amount}"

    @classmethod
    def calculate_fine(cls, order):
        # 1% penalty per day overdue based on the book's daily_price
        if order.status == Order.Status.OVERDUE and order.return_date and order.due_date:
            days_overdue = (order.return_date - order.due_date).days
            if days_overdue > 0:
                daily_price = order.copy.book.daily_price
                fine_per_day = daily_price * Decimal('0.01')
                total_fine = fine_per_day * days_overdue
                return total_fine
        return Decimal('0.00')
