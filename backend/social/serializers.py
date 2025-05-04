from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Like, Follow
from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.cache import cache

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'likes_count']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['user']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['follower']

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'followers_count']

    def get_followers_count(self, obj):
        cache_key = f"user_{obj.id}_followers_count"
        count = cache.get(cache_key)
        if count is None:
            count = obj.followers.count()
            cache.set(cache_key, count, timeout=60)
        return count