import uuid

from api.permissions import \
    AdminOnly  # AdminModeratorAuthorPermission,; IsAdminUserOrReadOnly,
from api.serializers import GetTokenSerializer  # NotAdminSerializer,
from api.serializers import SignUpSerializer, UserSerializer
from django.core.mail import EmailMessage
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated, AdminOnly]
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ['username']
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
    ]

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def my_profile(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            data = request.data.copy()
            if 'role' in data:
                del data['role']
            serializer = UserSerializer(request.user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        if not username:
            return Response(
                {'username': 'Имя пользователя обязательно!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound(detail='Пользователь не найден!')
        if not confirmation_code:
            return Response(
                {'confirmation_code': 'Код подтверждения обязателен!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if confirmation_code != user.confirmation_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = RefreshToken.for_user(user).access_token
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class APISignup(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_DNS, username))

        if User.objects.filter(email=email).exists():
            return Response(
                {'message': 'Пользователь с таким email уже существует'},
                status=status.HTTP_200_OK
            )

        try:
            user = serializer.save()
        except IntegrityError:
            return Response(
                {'message': 'Пользователь с такими данными уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.confirmation_code = confirmation_code
        user.save()
        email_body = (
            f'Здравствуйте, {user.username}.'
            f'\nКод подтверждения для доступа к API: {user.confirmation_code}')
        email = EmailMessage(
            subject='Код подтверждения для доступа к API!',
            body=email_body,
            to=[user.email],)
        email.send()
        return Response(serializer.data, status=status.HTTP_200_OK)


# class CategoryViewSet():
# permission_classes = (IsAdminUserOrReadOnly,)
# raise


# class GenreViewSet():
# permission_classes = (IsAdminUserOrReadOnly,)


# class TitleViewSet(ModelViewSet):
# permission_classes = (IsAdminUserOrReadOnly,)


# class CommentViewSet():
# permission_classes = (AdminModeratorAuthorPermission,)


# class ReviewViewSet():
# permission_classes = (AdminModeratorAuthorPermission,)
