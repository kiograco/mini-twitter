from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, FollowViewSet, UserViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'follows', FollowViewSet, basename='follow')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]