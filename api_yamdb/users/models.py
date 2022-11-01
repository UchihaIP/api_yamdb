from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLES = (
    ('User', 'Пользователь'), 
    ('Moderator', 'Модератор'), 
    ('Admin', 'Админ'), 
    ('Superuser', 'Суперпользователь')
)

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    user_role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        blank=True,
        default='User'
    )
