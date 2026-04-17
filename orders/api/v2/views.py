from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from orders.serializers import OrderSerializer
from users.permissions import IsUser, IsAdminOrOperator
from datetime import timedelta

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', 'user') in ['admin', 'operator']:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def get_permissions(self):
        if self.action == 'create':
            return [IsUser()]
        if self.action in ['update', 'partial_update', 'destroy', 'accept_order', 'return_order']:
            return [IsAdminOrOperator()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='booked')

    @action(detail=True, methods=['post'])
    def accept_order(self, request, pk=None):
        order = self.get_object()
        
        if order.status != 'booked':
            return Response({'detail': "Faqat band (booked) qilinganlar qabul qilinadi"}, status=status.HTTP_400_BAD_REQUEST)

        # 1 kun o'tib ketgan bo'lsa brondan yechish (o'chirish) qoidasi
        if timezone.now() > order.booked_at + timedelta(days=1):
            order.delete()
            return Response({'detail': "1 kun ichida olinmagani uchun brondan yechildi"}, status=status.HTTP_400_BAD_REQUEST)

        # Kunlik ijara olinadi, default 3 kun
        days = int(request.data.get('days', 3))
        
        order.status = 'borrowed'
        order.borrowed_at = timezone.now()
        order.due_date = order.borrowed_at + timedelta(days=days)
        order.save()
        
        return Response({'detail': "Kitob olib ketishga ruxsat berildi", 'due_date': order.due_date})

    @action(detail=True, methods=['post'])
    def return_order(self, request, pk=None):
        order = self.get_object()

        if order.status != 'borrowed':
            return Response({'detail': "Faqat olib ketilgan (borrowed) kitoblarni qaytarish mumkin"}, status=status.HTTP_400_BAD_REQUEST)

        now = timezone.now()
        fine = 0
        if order.due_date and now > order.due_date:
            late_days = (now - order.due_date).days
            if late_days > 0:
                daily_price = float(order.book.daily_price)
                fine = late_days * (daily_price * 0.01) # 1% jarima hisobi

        order.status = 'returned'
        order.fine_amount = fine
        order.save()
        
        return Response({'detail': "Kitob qaytarildi", 'fine_amount': fine})
