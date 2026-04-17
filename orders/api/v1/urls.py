from django.urls import path
from .views import OrderAPIView, OrderAcceptAPIView, OrderReturnAPIView

urlpatterns = [
    path('', OrderAPIView.as_view(), name='v1_order_list_create'),
    path('<int:pk>/accept/', OrderAcceptAPIView.as_view(), name='v1_order_accept'),
    path('<int:pk>/return/', OrderReturnAPIView.as_view(), name='v1_order_return'),
]