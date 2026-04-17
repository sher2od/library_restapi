from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# API V1 URLs (Raw SQL)
api_v1_patterns = [
    path('users/', include('users.api.v1.urls')),
    path('books/', include('books.api.v1.urls')),
    path('orders/', include('orders.api.v1.urls')),
]

# API V2 URLs (Django ORM)
api_v2_patterns = [
    path('users/', include('users.api.v2.urls')),
    path('books/', include('books.api.v2.urls')),
    path('orders/', include('orders.api.v2.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Versioned API Endpoints
    path('api/v1/', include((api_v1_patterns, 'v1'))),
    path('api/v2/', include((api_v2_patterns, 'v2'))),
]
