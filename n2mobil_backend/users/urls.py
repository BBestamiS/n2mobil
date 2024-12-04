from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.user_viewset import UserViewSet
from .views.todo_viewset import TodoViewSet
from .views.post_viewset import PostViewSet
from .views.album_viewset import AlbumViewSet
from .views.comment_viewset import CommentViewSet
from .views.photo_viewset import PhotoViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'todos', TodoViewSet, basename='todo')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'photos', PhotoViewSet, basename='photo')

urlpatterns = [
    path('', include(router.urls)),
]