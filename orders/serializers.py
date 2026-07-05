from rest_framework import serializers
from .models import Order, OrderItem
from inventory.models import BookCopy


class OrderItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='copy.book.title', read_only=True)
    barcode = serializers.CharField(source='copy.barcode', read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    copies = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=BookCopy.objects.all()),
        write_only=True,
        help_text="List of BookCopy IDs to borrow/reserve"
    )

    class Meta:
        model = Order
        fields = ['id', 'client', 'issued_by', 'borrow_date', 'due_date', 'reserved_until', 'status', 'notes', 'copies']
        read_only_fields = ('issued_by', 'status', 'borrow_date')

    def validate_copies(self, value):
        if not value:
            raise serializers.ValidationError("At least one book copy must be selected.")
        
        # Check if copies are available
        unavailable_copies = []
        for copy in value:
            if copy.status != BookCopy.Status.AVAILABLE:
                unavailable_copies.append(f"{copy.book.title} [{copy.barcode}]")
        
        if unavailable_copies:
            raise serializers.ValidationError(
                f"The following copies are not available: {', '.join(unavailable_copies)}"
            )
        return value


class OrderDetailSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.username', read_only=True)
    issued_by_name = serializers.CharField(source='issued_by.username', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
