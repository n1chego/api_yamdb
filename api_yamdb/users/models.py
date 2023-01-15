from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    ]

    email = models.EmailField(unique=True, verbose_name='email')
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name='Имя'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='информация о пользователе'
    )
    role = models.CharField(
        max_length=30, choices=ROLE_CHOICES, default=USER, verbose_name='Роль'
    )
    confirmation_code = models.TextField(
        null=True, verbose_name='код подтверждения'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return (
            self.role == 'admin'
            or self.is_superuser
            or self.is_staff
        )
