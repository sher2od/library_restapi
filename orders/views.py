from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from inventory.models import BookCopy
from .models import Order
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
        qs = Order.objects.select_related('copy__book', 'client', 'issued_by').all()
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
        copy = serializer.validated_data['copy']
        
        # Kitob bo'shmi tekshirish
        if copy.status != BookCopy.Status.AVAILABLE:
            raise ValidationError({'copy': 'This book copy is not available.'})
            
        # Librarian yoki Manager bo'lsa 'issued_by' o'zi bo'ladi
        issued_by = user if user.role in ('admin', 'manager', 'librarian') else None
        
        # Order yaratilganda kitob statusini 'borrowed' qilish
        copy.status = BookCopy.Status.BORROWED
        copy.save()
        
        serializer.save(issued_by=issued_by)
