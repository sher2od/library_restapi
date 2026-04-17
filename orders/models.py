from django.db import models
from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = (
        ('booked', 'Band'),
        ('borrowed', 'Olib ketilgan'),
        ('returned', 'Qaytarilgan'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    
    booked_at = models.DateTimeField(auto_now_add=True)
    borrowed_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id}: {self.user} - {self.book.title}"
