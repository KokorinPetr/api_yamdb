from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError

from .validators import validate_username

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
        db_index=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        db_index=True,
    )
    role = models.CharField(
        'роль', max_length=20, choices=ROLE_CHOICES, default=USER, blank=True
    )
    bio = models.TextField('биография', blank=True)
    first_name = models.CharField('имя', max_length=150, blank=True)
    last_name = models.CharField('фамилия', max_length=150, blank=True)
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        default='XXXX',
    )

    def validate_confirmation_code(self, value):
        if value != self.confirmation_code:
            raise ValidationError('Неверный код подтверждения!')

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    FIRST_NAME_FIELD = 'first_name'

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
