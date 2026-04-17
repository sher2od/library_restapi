from django.utils import timezone
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsUser, IsAdminOrOperator
from datetime import timedelta

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

class OrderAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsUser()]
        return [IsAuthenticated()]

    def get(self, request):
        user = request.user
        with connection.cursor() as cursor:
            if getattr(user, 'role', 'user') in ['admin', 'operator']:
                cursor.execute("SELECT * FROM orders_order")
            else:
                cursor.execute("SELECT * FROM orders_order WHERE user_id = %s", [user.id])
            orders = dictfetchall(cursor)
        return Response(orders)

    def post(self, request):
        book_id = request.data.get('book_id')
        user_id = request.user.id
        now = timezone.now()
        
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO orders_order (user_id, book_id, status, booked_at, fine_amount) VALUES (%s, %s, 'booked', %s, 0) RETURNING id",
                [user_id, book_id, now]
            )
            order_id = cursor.fetchone()[0]
            
        return Response({'id': order_id, 'status': 'booked'}, status=status.HTTP_201_CREATED)

class OrderAcceptAPIView(APIView):
    permission_classes = [IsAdminOrOperator]

    def post(self, request, pk):
        with connection.cursor() as cursor:
            cursor.execute("SELECT status, booked_at FROM orders_order WHERE id = %s", [pk])
            row = cursor.fetchone()
            if not row:
                return Response({'detail': "topilmadi"}, status=status.HTTP_404_NOT_FOUND)
                
            status_current, booked_at = row
            if status_current != 'booked':
                return Response({'detail': "Faqat 'booked' statusdagilarni qabul qilish mumkin."}, status=status.HTTP_400_BAD_REQUEST)
                
            if timezone.now() > booked_at + timedelta(days=1):
                cursor.execute("DELETE FROM orders_order WHERE id = %s", [pk])
                return Response({'detail': "1 kun o'tib ketgan zakaz yechildi."}, status=status.HTTP_400_BAD_REQUEST)

            days = int(request.data.get('days', 3))
            borrowed_at = timezone.now()
            due_date = borrowed_at + timedelta(days=days)
            
            cursor.execute(
                "UPDATE orders_order SET status = 'borrowed', borrowed_at = %s, due_date = %s WHERE id = %s",
                [borrowed_at, due_date, pk]
            )
        return Response({'detail': "Kitob foydalanishga berildi", 'due_date': due_date})

class OrderReturnAPIView(APIView):
    permission_classes = [IsAdminOrOperator]

    def post(self, request, pk):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT o.status, o.due_date, b.daily_price FROM orders_order o JOIN books_book b ON o.book_id = b.id WHERE o.id = %s", [pk]
            )
            row = cursor.fetchone()
            if not row:
                return Response({'detail': "Topilmadi"}, status=status.HTTP_404_NOT_FOUND)
                
            current_status, due_date, daily_price = row
            if current_status != 'borrowed':
                return Response({'detail': "Faqat 'borrowed' qilinganlarni qaytarish mumkin"}, status=status.HTTP_400_BAD_REQUEST)
                
            now = timezone.now()
            fine = 0
            if due_date and now > due_date:
                late_days = (now - due_date).days
                if late_days > 0:
                    fine = late_days * float(daily_price) * 0.01
                    
            cursor.execute(
                "UPDATE orders_order SET status = 'returned', fine_amount = %s WHERE id = %s",
                [fine, pk]
            )
            
        return Response({'detail': "Qaytarildi", 'fine_amount': fine})
