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

