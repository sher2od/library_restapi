from rest_framework import serializers
from .models import BookCopy
from library.serializers import BookListSerializer


class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = '__all__'


class BookCopyDetailSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)

    class Meta:
        model = BookCopy
        fields = '__all__'
