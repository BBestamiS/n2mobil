from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache
from users.models import Comment
from users.serializers import  CommentSerializer
from users.permissions import APIKeyPermission

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [APIKeyPermission]

    @swagger_auto_schema(
        operation_description="Tüm yorumları okuma servisi.",
        responses={
            200: "Başarılı: Yorumlar başarıyla getirildi.",
            500: "Sunucu hatası: Yorumlar getirilemedi."
        }
    )
    def list(self, request, *args, **kwargs):
        cache_key = "comments_list"
        cached_comments = cache.get(cache_key)

        if cached_comments:
            return Response(cached_comments)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 10) 
        return response

    @swagger_auto_schema(
        operation_description="Belirli yorumu okuma servisi.",
        responses={
            200: "Başarılı: Yorum başarıyla getirildi.",
            404: "Bulunamadı: Yorum mevcut değil.",
            500: "Sunucu hatası: Yorum getirilemedi."
        }
    )
    def retrieve(self, request, *args, **kwargs):
        comment_id = kwargs.get('pk')
        cache_key = f"comment_{comment_id}"
        cached_comment = cache.get(cache_key)

        if cached_comment:
            return Response(cached_comment)

        comment = get_object_or_404(Comment, pk=comment_id)
        serializer = self.get_serializer(comment)
        cache.set(cache_key, serializer.data, timeout=60 * 10)  
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Yeni yorum oluşturma servisi.",
        responses={
            201: "Başarılı: Yorum başarıyla oluşturuldu.",
            400: "Hatalı istek: Yorum oluşturulamadı.",
            500: "Sunucu hatası: Yorum oluşturulamadı."
        }
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete("comments_list") 
        return response

    @swagger_auto_schema(
        operation_description="Belirli yorumu silme servisi.",
        responses={
            204: "Başarılı: Yorum başarıyla silindi.",
            404: "Bulunamadı: Yorum mevcut değil.",
            500: "Sunucu hatası: Yorum silinemedi."
        }
    )
    def destroy(self, request, *args, **kwargs):
        comment_id = kwargs.get('pk')
        response = super().destroy(request, *args, **kwargs)
        cache.delete(f"comment_{comment_id}")  
        cache.delete("comments_list")  
        return response

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        pass
