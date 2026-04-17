from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserSerializer
from users.permissions import IsAdminOrOperator

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Yangi foydalanuvchi yaratish (registratsiya) hamma uchun ochiq
        if self.action == 'create':
            return [AllowAny()]
        # Qolgan funksiyalar asosan admin yoki operatorlarga
        return [IsAdminOrOperator()]
