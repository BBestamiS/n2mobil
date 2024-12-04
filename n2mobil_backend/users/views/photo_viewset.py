from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache
from users.models import Photo
from users.serializers import PhotoSerializer
from users.permissions import APIKeyPermission

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [APIKeyPermission]

    @swagger_auto_schema(
        operation_description="Tüm resimleri okuma servisi.",
        responses={
            200: "Başarılı: Fotoğraf listesi başarıyla getirildi.",
            500: "Sunucu hatası: Fotoğraf listesi getirilemedi."
        }
    )
    def list(self, request, *args, **kwargs):
        cache_key = "photos_list"
        cached_photos = cache.get(cache_key)

        if cached_photos:
            return Response(cached_photos)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 10)  
        return response

    @swagger_auto_schema(
        operation_description="Belirli fotoğrafı okuma servisi.",
        responses={
            200: "Başarılı: Fotoğraf başarıyla getirildi.",
            404: "Bulunamadı: Fotoğraf mevcut değil.",
            500: "Sunucu hatası: Fotoğraf getirilemedi."
        }
    )
    def retrieve(self, request, *args, **kwargs):
        photo_id = kwargs.get('pk')
        cache_key = f"photo_{photo_id}"
        cached_photo = cache.get(cache_key)

        if cached_photo:
            return Response(cached_photo)

        photo = get_object_or_404(Photo, pk=photo_id)
        serializer = self.get_serializer(photo)
        cache.set(cache_key, serializer.data, timeout=60 * 10) 
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Yeni fotoğraf oluşturma servisi.",
        responses={
            201: "Başarılı: Yeni fotoğraf başarıyla oluşturuldu.",
            400: "Hatalı istek: Fotoğraf oluşturulamadı.",
            500: "Sunucu hatası: Fotoğraf oluşturulamadı."
        }
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete("photos_list") 
        return response

    @swagger_auto_schema(
        operation_description="Belirli fotoğrafı silme servisi.",
        responses={
            204: "Başarılı: Fotoğraf başarıyla silindi.",
            404: "Bulunamadı: Fotoğraf mevcut değil.",
            500: "Sunucu hatası: Fotoğraf silinemedi."
        }
    )
    def destroy(self, request, *args, **kwargs):
        photo_id = kwargs.get('pk')
        response = super().destroy(request, *args, **kwargs)
        cache.delete(f"photo_{photo_id}")  
        cache.delete("photos_list")  
        return response

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        pass