from rest_framework import serializers
from orders.models import Order

class OrderSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(source='user', read_only=True)
    book_name = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
