from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache
from users.models import Post, Comment
from users.serializers import PostSerializer, CommentSerializer
from users.permissions import APIKeyPermission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [APIKeyPermission]

    @swagger_auto_schema(
        operation_description="Tüm postları okuma servisi.",
        responses={
            200: "Başarılı: Post listesi başarıyla getirildi.",
            500: "Sunucu hatası: Post listesi getirilemedi."
        }
    )
    def list(self, request, *args, **kwargs):
        cache_key = "posts_list"
        cached_posts = cache.get(cache_key)

        if cached_posts:
            return Response(cached_posts)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 10) 
        return response

    @swagger_auto_schema(
        operation_description="Belirli postu okuma servisi.",
        responses={
            200: "Başarılı: Post başarıyla getirildi.",
            404: "Bulunamadı: Post mevcut değil.",
            500: "Sunucu hatası: Post getirilemedi."
        }
    )
    def retrieve(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        cache_key = f"post_{post_id}"
        cached_post = cache.get(cache_key)

        if cached_post:
            return Response(cached_post)

        post = get_object_or_404(Post, pk=post_id)
        serializer = self.get_serializer(post)
        cache.set(cache_key, serializer.data, timeout=60 * 10)  
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Yeni post oluşturma servisi.",
        responses={
            201: "Başarılı: Yeni post başarıyla oluşturuldu.",
            400: "Hatalı istek: Post oluşturulamadı.",
            500: "Sunucu hatası: Post oluşturulamadı."
        }
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete("posts_list")  
        return response

    @swagger_auto_schema(
        operation_description="Belirli postu silme servisi.",
        responses={
            204: "Başarılı: Post başarıyla silindi.",
            404: "Bulunamadı: Post mevcut değil.",
            500: "Sunucu hatası: Post silinemedi."
        }
    )
    def destroy(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        response = super().destroy(request, *args, **kwargs)
        cache.delete(f"post_{post_id}") 
        cache.delete("posts_list")  
        return response

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        pass

    @action(detail=True, methods=['get'], url_path='comments')
    @swagger_auto_schema(
        operation_description="Belirli postun tüm yorumlarını okuma servisi.",
        responses={
            200: "Başarılı: Posta ait yorumlar başarıyla getirildi.",
            404: "Bulunamadı: Post mevcut değil.",
            500: "Sunucu hatası: Yorumlar getirilemedi."
        }
    )
    def comments(self, request, pk=None):
        cache_key = f"post_{pk}_comments"
        cached_comments = cache.get(cache_key)

        if cached_comments:
            return Response(cached_comments)

        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 10) 
        return Response(serializer.data)
