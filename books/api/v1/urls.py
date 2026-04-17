from django.urls import path
from .views import BookAPIView, BookDetailAPIView, RatingAPIView

urlpatterns = [
    path('', BookAPIView.as_view(), name='v1_book_list_create'),
    path('<int:pk>/', BookDetailAPIView.as_view(), name='v1_book_detail'),
    path('<int:book_id>/rate/', RatingAPIView.as_view(), name='v1_book_rate'),
]