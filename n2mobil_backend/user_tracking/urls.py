from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
from users.views import UserViewSet, TodoViewSet, PostViewSet, AlbumViewSet, CommentViewSet, PhotoViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'todos', TodoViewSet, basename='todo')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'photos', PhotoViewSet, basename='photo')

schema_view = get_schema_view(
    openapi.Info(
        title="N2Mobil API",
        default_version='v1',
        description="API documentation for N2Mobil with x-api-key authentication",
        contact=openapi.Contact(email="bestami980@outlook.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),  # Swagger'a herkes erişebilir
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]