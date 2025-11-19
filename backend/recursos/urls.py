from rest_framework.routers import DefaultRouter
from .views import RecursoViewSet

router = DefaultRouter()
router.register(r'recursos', RecursoViewSet)

urlpatterns = router.urls