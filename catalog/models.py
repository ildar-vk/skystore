from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name='Изображение',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        blank=True,
        null=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего изменения'
    )

    # НОВОЕ: Владелец продукта
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='products',
        null=True,
        blank=True
    )

    # НОВОЕ: Статус публикации
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликовано',
        help_text='Опубликован ли продукт'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']

        # НОВЫЕ: Кастомные права
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
            ('can_delete_any_product', 'Может удалять любой продукт'),
        ]

    def __str__(self):
        return f"{self.name} - {self.price}"