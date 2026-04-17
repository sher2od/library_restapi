from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from books.models import Book, Rating
from books.serializers import BookSerializer, RatingSerializer
from users.permissions import IsAdminOrOperator, IsUser
from orders.models import Order

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrOperator()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['post'], permission_classes=[IsUser])
    def rate(self, request, pk=None):
        book = self.get_object()
        user = request.user
        
        # Tekshiruv: Foydalanuvchi bu kitobni o'qib qaytarganmi
        read_book = Order.objects.filter(user=user, book=book, status='returned').exists()
        if not read_book:
            return Response({'detail': "Siz bu kitobni o'qimagansiz"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Tekshiruv: Oldin baho berganmi
        if Rating.objects.filter(user=user, book=book).exists():
            return Response({'detail': "Allaqachon baho bergansiz"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user, book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
