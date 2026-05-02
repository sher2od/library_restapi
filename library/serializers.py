from rest_framework import serializers
from .models import Branch, Author, Genre, Book


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    genre_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_author_name(self, obj):
        return str(obj.author) if obj.author else None

    def get_genre_name(self, obj):
        return obj.genre.name if obj.genre else None


class BookListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'genre', 'daily_price', 'branch')
