from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Branch, Author, Genre, Book, Rating
from .serializers import BranchSerializer, AuthorSerializer, GenreSerializer, BookSerializer, BookListSerializer, RatingSerializer
from .permissions import IsAdminOrManager


@extend_schema_view(
    list=extend_schema(tags=['Library: Branches']),
    create=extend_schema(tags=['Library: Branches']),
    retrieve=extend_schema(tags=['Library: Branches']),
    update=extend_schema(tags=['Library: Branches']),
    partial_update=extend_schema(tags=['Library: Branches']),
    destroy=extend_schema(tags=['Library: Branches']),
)
class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAdminOrManager]


@extend_schema_view(
    list=extend_schema(tags=['Library: Authors']),
    create=extend_schema(tags=['Library: Authors']),
    retrieve=extend_schema(tags=['Library: Authors']),
    update=extend_schema(tags=['Library: Authors']),
    partial_update=extend_schema(tags=['Library: Authors']),
    destroy=extend_schema(tags=['Library: Authors']),
)
class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrManager]


@extend_schema_view(
    list=extend_schema(tags=['Library: Genres']),
    create=extend_schema(tags=['Library: Genres']),
    retrieve=extend_schema(tags=['Library: Genres']),
    update=extend_schema(tags=['Library: Genres']),
    partial_update=extend_schema(tags=['Library: Genres']),
    destroy=extend_schema(tags=['Library: Genres']),
)
class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrManager]


@extend_schema_view(
    list=extend_schema(tags=['Library: Books']),
    create=extend_schema(tags=['Library: Books']),
    retrieve=extend_schema(tags=['Library: Books']),
    update=extend_schema(tags=['Library: Books']),
    partial_update=extend_schema(tags=['Library: Books']),
    destroy=extend_schema(tags=['Library: Books']),
)
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


@extend_schema_view(
    list=extend_schema(tags=['Library: Ratings']),
    create=extend_schema(tags=['Library: Ratings']),
    retrieve=extend_schema(tags=['Library: Ratings']),
    update=extend_schema(tags=['Library: Ratings']),
    partial_update=extend_schema(tags=['Library: Ratings']),
    destroy=extend_schema(tags=['Library: Ratings']),
)
class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    # Allow read for all, but only authenticated users can rate
    def get_permissions(self):
        from rest_framework.permissions import AllowAny, IsAuthenticated
        if self.action in ('list', 'retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

