from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache
from users.models import User, Todo, Post, Album
from users.serializers import UserSerializer, TodoSerializer, PostSerializer, AlbumSerializer
from users.permissions import APIKeyPermission

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [APIKeyPermission]

    @swagger_auto_schema(
        operation_description="Tüm TODO'ları okuma servisi.",
        responses={
            200: "Başarılı: Tüm todolar başarıyla listelendi.",
            500: "Sunucu hatası: Todolar listelenemedi."
        }
    )
    def list(self, request, *args, **kwargs):
        cache_key = "todos_list"
        cached_todos = cache.get(cache_key)

        if cached_todos:
            return Response(cached_todos)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 10) 
        return response

    @swagger_auto_schema(
        operation_description="Belirli TODO'yu okuma servisi.",
        responses={
            200: "Başarılı: Belirtilen todo başarıyla getirildi.",
            404: "Bulunamadı: Belirtilen todo mevcut değil.",
            500: "Sunucu hatası: Todo getirilemedi."
        }
    )
    def retrieve(self, request, *args, **kwargs):
        todo_id = kwargs.get('pk')
        cache_key = f"todo_{todo_id}"
        cached_todo = cache.get(cache_key)

        if cached_todo:
            return Response(cached_todo)

        todo = get_object_or_404(Todo, pk=todo_id)
        serializer = self.get_serializer(todo)
        cache.set(cache_key, serializer.data, timeout=60 * 10)  
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Yeni TODO oluşturma servisi.",
        responses={
            201: "Başarılı: Yeni todo oluşturuldu.",
            400: "Geçersiz istek: Todo oluşturulamadı.",
            500: "Sunucu hatası: Todo oluşturulamadı."
        }
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete("todos_list")  
        return response

    @swagger_auto_schema(
        operation_description="Belirli TODO'yu silme servisi",
        responses={
            204: "Başarılı: Todo başarıyla silindi.",
            404: "Bulunamadı: Todo mevcut değil.",
            500: "Sunucu hatası: Todo silinemedi."
        }
    )
    def destroy(self, request, *args, **kwargs):
        todo_id = kwargs.get('pk')
        response = super().destroy(request, *args, **kwargs)
        cache.delete(f"todo_{todo_id}") 
        cache.delete("todos_list")  
        return response

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        pass
