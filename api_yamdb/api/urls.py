from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='api'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='api'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
