from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # JWT responsega foydalanuvchi rolini qo'shamiz
        data['role'] = self.user.role
        return data


@extend_schema(tags=['Authentication'])
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserSerializer
from .models import User


@extend_schema(tags=['Authentication'], responses={201: UserSerializer})
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

