from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StatViewSet, TrajOptViewSet

router = DefaultRouter()
router.register(r'stats', StatViewSet)
router.register(r'trajopt', TrajOptViewSet)

urlpatterns = [
    path('', include(router.urls)),
]