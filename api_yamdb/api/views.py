import uuid

from api.permissions import \
    AdminOnly  # AdminModeratorAuthorPermission,; IsAdminUserOrReadOnly,
from api.serializers import GetTokenSerializer  # NotAdminSerializer,
from api.serializers import SignUpSerializer, UserSerializer
from django.core.mail import EmailMessage
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
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
    lookup_field = "username"
    filter_backends = [SearchFilter]
    search_fields = ["username"]
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
    ]

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == "PATCH":
            data = request.data.copy()
            if "role" in data:
                del data["role"]  # Remove the 'role' key from the data
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
            user = User.objects.get(username=data["username"])
        except User.DoesNotExist:
            return Response(
                {"username": "Пользователь не найден!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if not data.get("confirmation_code"):
            return Response(
                {"confirmation_code": "Код подтверждения обязателен!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if data["confirmation_code"] != user.confirmation_code:
            raise AuthenticationFailed("Неверный код подтверждения!")

        token = RefreshToken.for_user(user).access_token
        return Response({"token": str(token)}, status=status.HTTP_201_CREATED)


class APISignup(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        confirmation_code = str(
            uuid.uuid3(uuid.NAMESPACE_DNS, username)
        )  # Генерируем код подтверждения
        try:
            user, created = User.objects.get_or_create(
                **serializer.validated_data
            )
        except Exception as error:
            return Response(
                f"Ошибка {error}",
                status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = confirmation_code
        user.save()
        email_body = (
            f"Здравствуйте, {user.username}."
            f"\nКод подтверждения для доступа к API: \
            {user.confirmation_code}"
        )
        email = EmailMessage(
            subject="Код подтверждения для доступа к API!",
            body=email_body,
            to=[user.email],
        )
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
