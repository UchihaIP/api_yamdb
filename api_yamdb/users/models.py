from django.contrib.auth.models import AbstractUser
from django.db import models
from random import randint

RANDOM_CONFIRMATION_CODE = randint(1000,9999)

USER_ROLES = (
    ('User', 'Пользователь'),
    ('Moderator', 'Модератор'),
    ('Admin', 'Админ'),
    ('Superuser', 'Суперпользователь')
)


class User(AbstractUser):
    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Уникальное имя пользователя'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Имеил пользователя'
    )
    role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        blank=True,
        default='User',
        verbose_name='Роль пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    confirmation_code = models.CharField(
        max_length=5,
        null=True
    )

    @property
    def is_user(self):
        return self.role == 'User'

    @property
    def is_moderator(self):
        return self.role == 'Moderator'

    @property
    def is_admin(self):
        return self.role == 'Admin'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            ),
        ]

    def __str__(self):
        return self.username
