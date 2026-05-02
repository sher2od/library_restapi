from django.db import models
from django.conf import settings
from inventory.models import BookCopy


class Order(models.Model):
    class Status(models.TextChoices):
        RESERVED = 'reserved', 'Reserved'
        ACTIVE = 'active', 'Active'
        RETURNED = 'returned', 'Returned'
        OVERDUE = 'overdue', 'Overdue'
        LOST = 'lost', 'Lost'
        CANCELED = 'canceled', 'Canceled'

    copy = models.ForeignKey(BookCopy, on_delete=models.PROTECT, related_name='orders')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='borrowed_books')
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='issued_books'
    )
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-borrow_date']

    def __str__(self):
        return f"Order #{self.id} - {self.client.username} ({self.status})"
