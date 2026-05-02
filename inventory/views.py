from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema
from library.permissions import IsAdminOrManager
from .models import BookCopy
from .serializers import BookCopySerializer, BookCopyDetailSerializer


@extend_schema_view(
    list=extend_schema(tags=['Inventory']),
    create=extend_schema(tags=['Inventory']),
    retrieve=extend_schema(tags=['Inventory']),
    update=extend_schema(tags=['Inventory']),
    partial_update=extend_schema(tags=['Inventory']),
    destroy=extend_schema(tags=['Inventory']),
)
class BookCopyViewSet(ModelViewSet):
    queryset = BookCopy.objects.select_related('book', 'book__author', 'book__branch').all()
    permission_classes = [IsAdminOrManager]

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return BookCopyDetailSerializer
        return BookCopySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        book = self.request.query_params.get('book')
        status = self.request.query_params.get('status')
        condition = self.request.query_params.get('condition')
        branch = self.request.query_params.get('branch')
        if book:
            qs = qs.filter(book_id=book)
        if status:
            qs = qs.filter(status=status)
        if condition:
            qs = qs.filter(condition=condition)
        if branch:
            qs = qs.filter(book__branch_id=branch)
        return qs

