from django.contrib.auth.models import AbstractUser
from django.db import models

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
