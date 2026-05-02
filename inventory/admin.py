from django.contrib import admin
from .models import BookCopy


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ('book', 'barcode', 'condition', 'status', 'acquired_date')
    list_filter = ('status', 'condition', 'book__branch')
    search_fields = ('barcode', 'book__title')
