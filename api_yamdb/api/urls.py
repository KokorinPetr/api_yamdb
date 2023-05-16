from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryCreateListDestroyViewSet,
    CommentViewSet,
    GenreCreateListDestroyViewSet,
    ReviewViewSet,
    TitleViewSet,
)

v1_router = routers.DefaultRouter()
v1_router.register(
    'categories',
    CategoryCreateListDestroyViewSet,
    basename='categories',
)
v1_router.register(
    'genres',
    GenreCreateListDestroyViewSet,
    basename='genres',
)
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='api',
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='api',
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
