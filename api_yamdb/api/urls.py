from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryDestroyView,
    CategoryListCreateView,
    GenreDestroyView,
    GenreListCreateView,
    TitleViewSet,
)

v1_router = routers.DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/categories/', CategoryListCreateView.as_view()),
    path('v1/categories/<slug:slug>/', CategoryDestroyView.as_view()),
    path('v1/genres/', GenreListCreateView.as_view()),
    path('v1/genres/<slug:slug>/', GenreDestroyView.as_view()),
]
