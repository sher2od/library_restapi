from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer
from library.permissions import IsAdminOrManager


@extend_schema_view(
    list=extend_schema(tags=['Finance']),
    create=extend_schema(tags=['Finance']),
    retrieve=extend_schema(tags=['Finance']),
    update=extend_schema(tags=['Finance']),
    partial_update=extend_schema(tags=['Finance']),
    destroy=extend_schema(tags=['Finance']),
)
class PaymentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Payment.objects.all()
        # Mijoz faqat o'zining to'lovlarini ko'radi
        if user.role == 'client':
            qs = qs.filter(order__client=user)
        return qs
