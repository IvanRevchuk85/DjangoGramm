from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from PIL import Image, UnidentifiedImageError
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField


User = get_user_model()


class Post(models.Model):
    """Модель поста"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    content = models.TextField(
        blank=True, null=True, verbose_name="Текст поста")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления")
    likes = models.ManyToManyField(
        User, related_name='liked_posts', blank=True
    )
    image = CloudinaryField('image', blank=True, null=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"


def validate_image(image):
    """Проверяет, является ли файл изображением"""
    try:
        img = Image.open(image)
        img.verify()  # Проверка, является ли файл корректным изображением
    except (UnidentifiedImageError, OSError):
        raise ValidationError("Загружаемый файл не является изображением!")


class PostImage(models.Model):
    """Модель изображений к постам с превью"""
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='images'
    )
    image = CloudinaryField(verbose_name="Изображение")
    thumbnail = CloudinaryField(
        blank=True, null=True, verbose_name="Превью изображения")

    def save(self, *args, **kwargs):
        """Создание превью перед сохранением"""
        super().save(*args, **kwargs)  # Сохраняем оригинальное изображение

        if self.image:
            try:
                # Присваиваем изображению превью, Cloudinary сам создаст уменьшенную версию
                self.thumbnail = self.image
                super().save(update_fields=['thumbnail'])
            except Exception as e:
                print(f"Ошибка при создании превью: {e}")

    class Meta:
        verbose_name = "Изображение поста"
        verbose_name_plural = "Изображения постов"

    def __str__(self):
        return f"Image for Post {self.post.id}"


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(max_length=50, unique=True,
                            verbose_name="Название тега")
    posts = models.ManyToManyField(
        Post, related_name='tags', blank=True, verbose_name="Посты с этим тегом"
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name
