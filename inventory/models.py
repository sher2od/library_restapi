from django.db import models
from library.models import Book


class BookCopy(models.Model):
    class Condition(models.TextChoices):
        EXCELLENT = 'excellent', 'Excellent'
        GOOD = 'good', 'Good'
        WORN = 'worn', 'Worn'
        DAMAGED = 'damaged', 'Damaged'

    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        BORROWED = 'borrowed', 'Borrowed'
        RESERVED = 'reserved', 'Reserved'
        RETIRED = 'retired', 'Retired'

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies')
    barcode = models.CharField(max_length=50, unique=True)
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.GOOD)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    acquired_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Book Copies'

    def __str__(self):
        return f"{self.book.title} [{self.barcode}]"
