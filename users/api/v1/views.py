from django.db import connection
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from users.permissions import IsAdminOrOperator

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

class UserAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAdminOrOperator()]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, username, role, is_active FROM users_user")
            users = dictfetchall(cursor)
        return Response(users)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role', 'user')
        
        if not username or not password:
            return Response({'detail': "Username va password kerak"}, status=status.HTTP_400_BAD_REQUEST)
            
        hashed_password = make_password(password)
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM users_user WHERE username = %s", [username])
            if cursor.fetchone():
                return Response({'detail': "Bunday foydalanuvchi mavjud"}, status=status.HTTP_400_BAD_REQUEST)
                
            cursor.execute(
                """
                INSERT INTO users_user (username, password, role, is_active, is_staff, is_superuser, date_joined)
                VALUES (%s, %s, %s, True, False, False, NOW()) RETURNING id
                """,
                [username, hashed_password, role]
            )
            new_id = cursor.fetchone()[0]
            
        return Response({'id': new_id, 'username': username, 'role': role}, status=status.HTTP_201_CREATED)
