from rest_framework.routers import DefaultRouter
from .views import BranchViewSet, AuthorViewSet, GenreViewSet, BookViewSet, RatingViewSet

app_name = 'library'

router = DefaultRouter()
router.register('branches', BranchViewSet)
router.register('authors', AuthorViewSet)
router.register('genres', GenreViewSet)
router.register('books', BookViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = router.urls
