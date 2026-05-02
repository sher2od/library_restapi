from rest_framework.viewsets import ModelViewSet
from .models import Branch, Author, Genre, Book
from .serializers import BranchSerializer, AuthorSerializer, GenreSerializer, BookSerializer, BookListSerializer
from .permissions import IsAdminOrManager


class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAdminOrManager]


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrManager]


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrManager]


class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('author', 'genre', 'branch').all()
    permission_classes = [IsAdminOrManager]

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        branch = self.request.query_params.get('branch')
        genre = self.request.query_params.get('genre')
        author = self.request.query_params.get('author')
        if branch:
            qs = qs.filter(branch_id=branch)
        if genre:
            qs = qs.filter(genre_id=genre)
        if author:
            qs = qs.filter(author_id=author)
        return qs
