# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя, наследуемая от AbstractUser
    """
    # Отключаем поле username, используем email для авторизации
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта'
    )

    # Дополнительные поля
    avatar = models.ImageField(
        upload_to='users/avatars/',
        verbose_name='Аватар',
        blank=True,
        null=True,
        help_text='Загрузите изображение (до 5MB)'
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name='Номер телефона',
        blank=True,
        null=True,
        help_text='В формате: +7 (XXX) XXX-XX-XX'
    )
    country = models.CharField(
        max_length=100,
        verbose_name='Страна',
        blank=True,
        null=True,
        help_text='Укажите вашу страну'
    )

    # Указываем поле для авторизации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Больше не требуется username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Возвращает полное имя или email, если имя не указано"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    def get_short_name(self):
        """Возвращает короткое имя или email"""
        return self.first_name or self.email
