from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .utils import Role


class User(AbstractUser):
    """Модель пользователя с расширенным функционалом для Django приложения."""

    USERNAME_REGEX = r"^[\w]+[^@\.\+\-]*$"

    username = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message="Неверное имя пользователя. "
                "Допускаются только буквы, цифры и знак подчеркивания."
                " Не может содержать символы «@», «.», «+» или «-».",
            )
        ],
        error_messages={
            "unique": "Пользователь с таким именем уже существует.",
        },
    )

    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="Имя", max_length=150, blank=True
    )
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=150, blank=True
    )
    bio = models.TextField(verbose_name="Биография", blank=True)
    role = models.CharField(
        verbose_name="Роль",
        max_length=20,
        choices=Role.get_role_choices(),
        default="user",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

        constraints = [
            models.UniqueConstraint(
                fields=("username", "email"), name="unique_username&email"
            )
        ]

    @property
    def is_admin(self):
        """Возвращает True, если пользователь является администратором."""
        return self.role == Role.admin.name

    def __str__(self):
        return self.username
