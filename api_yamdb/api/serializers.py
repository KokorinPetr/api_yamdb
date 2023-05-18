from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)


class SignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(max_length=150,
                                      regex=r'^[\w.@+-]+\Z', required=True)
    email = serializers.EmailField(max_length=254)

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"], email=validated_data["email"]
        )

    def validate_username(self, username):
        if username == "me":
            raise serializers.ValidationError(
                "Использование 'me' в качестве username нельзя."
            )
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            user = get_object_or_404(User, email=email)
            if self.initial_data.get("username") != user.username:
                raise serializers.ValidationError(
                    "Указана почта существующего пользователя!"
                )
        return email


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, attrs):
        self.instance.validate_confirmation_code(attrs["confirmation_code"])
        return attrs

    class Meta:
        model = User
        fields = ("username", "confirmation_code")
