from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryCreateListDestroyViewSet,
    GenreCreateListDestroyViewSet,
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

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
