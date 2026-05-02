from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('issued_by', 'status', 'return_date', 'borrow_date')


class OrderDetailSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.username', read_only=True)
    issued_by_name = serializers.CharField(source='issued_by.username', read_only=True)
    book_title = serializers.CharField(source='copy.book.title', read_only=True)
    barcode = serializers.CharField(source='copy.barcode', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
