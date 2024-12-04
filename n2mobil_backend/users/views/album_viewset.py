from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache
from users.models import  Album,Photo
from users.serializers import  AlbumSerializer, PhotoSerializer
from users.permissions import APIKeyPermission

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [APIKeyPermission]

    @swagger_auto_schema(
        operation_description="Tüm albümleri okuma servisi.",
        responses={
            200: "Başarılı: Albüm listesi başarıyla getirildi.",
            500: "Sunucu hatası: Albüm listesi getirilemedi."
        }
    )
    def list(self, request, *args, **kwargs):
        cache_key = "albums_list"
        cached_albums = cache.get(cache_key)

        if cached_albums:
            return Response(cached_albums)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 10)  
        return response

    @swagger_auto_schema(
        operation_description="Belirli albümü okuma serivis.",
        responses={
            200: "Başarılı: Albüm başarıyla getirildi.",
            404: "Bulunamadı: Albüm mevcut değil.",
            500: "Sunucu hatası: Albüm getirilemedi."
        }
    )
    def retrieve(self, request, *args, **kwargs):
        album_id = kwargs.get('pk')
        cache_key = f"album_{album_id}"
        cached_album = cache.get(cache_key)

        if cached_album:
            return Response(cached_album)

        album = get_object_or_404(Album, pk=album_id)
        serializer = self.get_serializer(album)
        cache.set(cache_key, serializer.data, timeout=60 * 10)  
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Yeni albüm oluşturma servisi.",
        responses={
            201: "Başarılı: Albüm başarıyla oluşturuldu.",
            400: "Hatalı istek: Albüm oluşturulurken hata oluştu.",
            500: "Sunucu hatası: Albüm oluşturulamadı."
        }
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete("albums_list") 
        return response

    @swagger_auto_schema(
        operation_description="Belirli albümü silme servisi.",
        responses={
            204: "Başarılı: Albüm başarıyla silindi.",
            404: "Bulunamadı: Albüm mevcut değil.",
            500: "Sunucu hatası: Albüm silinemedi."
        }
    )
    def destroy(self, request, *args, **kwargs):
        album_id = kwargs.get('pk')
        response = super().destroy(request, *args, **kwargs)
        cache.delete(f"album_{album_id}")  
        cache.delete("albums_list")  
        return response

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        pass

    @action(detail=True, methods=['get'], url_path='photos')
    @swagger_auto_schema(
        operation_description="Belirli albüme ait tüm fotoğrafları okuma servisi.",
        responses={
            200: "Başarılı: Albüme ait fotoğraflar başarıyla getirildi.",
            404: "Bulunamadı: Albüm mevcut değil.",
            500: "Sunucu hatası: Fotoğraflar getirilemedi."
        }
    )
    def photos(self, request, pk=None):
        cache_key = f"album_{pk}_photos"
        cached_photos = cache.get(cache_key)

        if cached_photos:
            return Response(cached_photos)

        album = get_object_or_404(Album, pk=pk)
        photos = Photo.objects.filter(album=album)
        serializer = PhotoSerializer(photos, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 10)  
        return Response(serializer.data)
