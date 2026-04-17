from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminOrOperator, IsUser

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

class BookAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminOrOperator()]
        return [IsAuthenticated()]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, daily_price FROM books_book")
            books = dictfetchall(cursor)
        return Response(books)

    def post(self, request):
        title = request.data.get('title')
        daily_price = request.data.get('daily_price')
        
        if not title or not daily_price:
            return Response({'detail': "Barcha maydonlarni to'ldiring"}, status=status.HTTP_400_BAD_REQUEST)
            
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO books_book (title, daily_price) VALUES (%s, %s) RETURNING id",
                [title, daily_price]
            )
            new_id = cursor.fetchone()[0]
            
        return Response({'id': new_id, 'title': title, 'daily_price': daily_price}, status=status.HTTP_201_CREATED)

class BookDetailAPIView(APIView):
    permission_classes = [IsAdminOrOperator]
    
    def put(self, request, pk):
        title = request.data.get('title')
        daily_price = request.data.get('daily_price')
        
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE books_book SET title = %s, daily_price = %s WHERE id = %s",
                [title, daily_price, pk]
            )
            if cursor.rowcount == 0:
                return Response({'detail': "Topilmadi"}, status=status.HTTP_404_NOT_FOUND)
                
        return Response({'id': pk, 'title': title, 'daily_price': daily_price})

    def delete(self, request, pk):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM books_book WHERE id = %s", [pk])
            if cursor.rowcount == 0:
                return Response({'detail': "Topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

class RatingAPIView(APIView):
    permission_classes = [IsUser]

    def post(self, request, book_id):
        user_id = request.user.id
        score = request.data.get('score')
        
        try:
            score = int(score)
            if score < 0 or score > 5:
                return Response({'detail': "Baho 0-5 gacha bo'lishi kerak"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'detail': "Noto'g'ri baho"}, status=status.HTTP_400_BAD_REQUEST)
            
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM orders_order WHERE user_id = %s AND book_id = %s AND status = 'returned'",
                [user_id, book_id]
            )
            if not cursor.fetchone():
                return Response({'detail': "Siz bu kitobni o'qimagansiz"}, status=status.HTTP_400_BAD_REQUEST)
                
            cursor.execute(
                "SELECT id FROM books_rating WHERE user_id = %s AND book_id = %s",
                [user_id, book_id]
            )
            if cursor.fetchone():
                return Response({'detail': "Allaqachon baho bergansiz"}, status=status.HTTP_400_BAD_REQUEST)
                
            cursor.execute(
                "INSERT INTO books_rating (user_id, book_id, score) VALUES (%s, %s, %s)",
                [user_id, book_id, score]
            )
            
        return Response({'detail': "Baho saqlandi"}, status=status.HTTP_201_CREATED)
