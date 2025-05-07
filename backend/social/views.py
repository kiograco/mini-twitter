from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Post, Like, Follow
from .serializers import PostSerializer, LikeSerializer, FollowSerializer, UserSerializer
from rest_framework.throttling import AnonRateThrottle
from .throttles import BurstRateThrottle


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [BurstRateThrottle, AnonRateThrottle]
    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        # Invalida o cache do feed após criação de post
        cache_key = f"user_feed_{self.request.user.id}"
        cache.delete(cache_key)
        return post

    def list(self, request, *args, **kwargs):
        cache_key = f"user_feed_{request.user.id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)

        # Cache do feed por 60 segundos
        cache.set(cache_key, response.data, timeout=60)
        return response

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

        # Opcional: invalidar cache se quiser refletir likes imediatamente
        cache_key = f"user_feed_{request.user.id}"
        cache.delete(cache_key)

        return Response({'detail': 'Post liked'})


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        following_user = serializer.validated_data['following']
        if following_user == self.request.user:
            raise ValidationError("You cannot follow yourself.")
        
        follow = serializer.save(follower=self.request.user)

        # Invalida contador de seguidores do usuário seguido
        followed_user_id = follow.following.id
        cache.delete(f"user_{followed_user_id}_followers_count")

        return follow


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]