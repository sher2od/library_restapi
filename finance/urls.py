from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet

app_name = 'finance'

router = DefaultRouter()
router.register('payments', PaymentViewSet, basename='payment')

urlpatterns = router.urls
