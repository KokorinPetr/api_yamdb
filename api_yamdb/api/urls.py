from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import APIGetToken, APISignup, UserViewSet

app_name = 'api'
router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
urlpatterns = [
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
