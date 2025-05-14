from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KudoViewSet, UserViewSet

router = DefaultRouter()
router.register(r'kudos', KudoViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
