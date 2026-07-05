from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from inventory.models import BookCopy
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderDetailSerializer


@extend_schema_view(
    list=extend_schema(tags=['Orders']),
    create=extend_schema(tags=['Orders']),
    retrieve=extend_schema(tags=['Orders']),
    update=extend_schema(tags=['Orders']),
    partial_update=extend_schema(tags=['Orders']),
    destroy=extend_schema(tags=['Orders']),
)
class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        qs = Order.objects.prefetch_related('items__copy__book').select_related('client', 'issued_by').all()
        # Mijoz faqat o'zining buyurtmalarini ko'radi, Admin/Manager hammasini ko'radi
        if user.role == 'client':
            qs = qs.filter(client=user)
        
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)
            
        return qs

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        user = self.request.user
        copies = serializer.validated_data.pop('copies')
        
        # Librarian yoki Manager bo'lsa 'issued_by' o'zi bo'ladi
        issued_by = user if user.role in ('admin', 'manager', 'librarian') else None
        
        # Agar reserved_until berilgan bo'lsa statusni reserved qilamiz
        reserved_until = serializer.validated_data.get('reserved_until')
        status = Order.Status.RESERVED if reserved_until else Order.Status.ACTIVE
        
        order = serializer.save(issued_by=issued_by, status=status)
        
        for copy in copies:
            copy.status = BookCopy.Status.RESERVED if status == Order.Status.RESERVED else BookCopy.Status.BORROWED
            copy.save()
        
            OrderItem.objects.create(
                order=order,
                copy=copy,
                status=OrderItem.Status.RESERVED if status == Order.Status.RESERVED else OrderItem.Status.ACTIVE
            )
