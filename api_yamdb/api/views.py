import uuid

from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import (
    AdminModeratorAuthorPermission,
    AdminOnly,
    IsAdminUserOrReadOnly,
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadOnlySerializer,
    TitleSerializer,
    UserSerializer,
)
from reviews.models import Category, Genre, Review, Title, User


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
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            data = request.data.copy()
            if 'role' in data:
                del data['role']  # Remove the 'role' key from the data
            serializer = UserSerializer(request.user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND,
            )
        if not data.get('confirmation_code'):
            return Response(
                {'confirmation_code': 'Код подтверждения обязателен!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if data['confirmation_code'] != user.confirmation_code:
            raise AuthenticationFailed('Неверный код подтверждения!')

        token = RefreshToken.for_user(user).access_token
        return Response({'token': str(token)}, status=status.HTTP_201_CREATED)


class APISignup(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = str(
            uuid.uuid3(uuid.NAMESPACE_DNS, username),
        )
        try:
            user, created = User.objects.get_or_create(
                **serializer.validated_data,
            )
        except Exception as error:
            return Response(
                f'Ошибка {error}',
                status=status.HTTP_400_BAD_REQUEST,
            )
        confirmation_code = confirmation_code
        user.save()
        email_body = (
            f'Здравствуйте, {user.username}.'
            f'\nКод подтверждения для доступа к API: \
            {user.confirmation_code}'
        )
        email = EmailMessage(
            subject='Код подтверждения для доступа к API!',
            body=email_body,
            to=[user.email],
        )
        email.send()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryCreateListDestroyViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreCreateListDestroyViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleReadOnlySerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    @property
    def title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.title,
        )

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Запрещено изменение чужого контента')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Запрещено удаление чужого контента')
        super().perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    @property
    def review_for_comment(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.review_for_comment.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.review_for_comment,
        )

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Запрещено изменение чужого контента')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Запрещено удаление чужого контента')
        super().perform_destroy(instance)
