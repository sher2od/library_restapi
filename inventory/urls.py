from rest_framework.routers import DefaultRouter
from .views import BookCopyViewSet

app_name = 'inventory'

router = DefaultRouter()
router.register('copies', BookCopyViewSet)

urlpatterns = router.urls
