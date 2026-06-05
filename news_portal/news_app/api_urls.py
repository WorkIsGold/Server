from rest_framework.routers import DefaultRouter
from .viewsets import UserViewSet, NewsViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'news', NewsViewSet, basename='news')

#urlpatterns = router.urls