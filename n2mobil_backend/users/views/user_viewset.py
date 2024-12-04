from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache
from users.models import User, Todo, Post, Album
from users.serializers import UserSerializer, TodoSerializer, PostSerializer, AlbumSerializer
from users.permissions import APIKeyPermission


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [APIKeyPermission]

    def list(self, request, *args, **kwargs):
        cache_key = "users_list"
        cached_users = cache.get(cache_key)

        if cached_users:
            return Response(cached_users)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 10) 
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete("users_list")  
        return response

    def destroy(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        cache.delete(f"user_{user_id}")
        cache.delete("users_list")  

        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        cache_key = f"user_{user_id}"
        cached_user = cache.get(cache_key)

        if cached_user:
            return Response(cached_user)

        user = get_object_or_404(User, pk=user_id)
        serializer = self.get_serializer(user)
        cache.set(cache_key, serializer.data, timeout=60 * 10)  
        return Response(serializer.data)
    
    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        pass
    

    @action(detail=True, methods=['get'], url_path='todos')
    def todos(self, request, pk=None):
        cache_key = f"user_{pk}_todos"
        cached_todos = cache.get(cache_key)

        if cached_todos:
            return Response(cached_todos)

        user = get_object_or_404(User, pk=pk)
        todos = Todo.objects.filter(user=user)
        serializer = TodoSerializer(todos, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 10)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='posts')
    def posts(self, request, pk=None):
        cache_key = f"user_{pk}_posts"
        cached_posts = cache.get(cache_key)

        if cached_posts:
            return Response(cached_posts)

        user = get_object_or_404(User, pk=pk)
        posts = Post.objects.filter(user=user)
        serializer = PostSerializer(posts, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 10)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='albums')
    def albums(self, request, pk=None):
        cache_key = f"user_{pk}_albums"
        cached_albums = cache.get(cache_key)

        if cached_albums:
            return Response(cached_albums)

        user = get_object_or_404(User, pk=pk)
        albums = Album.objects.filter(user=user)
        serializer = AlbumSerializer(albums, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 10)  
        return Response(serializer.data)
