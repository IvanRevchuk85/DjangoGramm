from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    email = models.EmailField(unique=True, verbose_name="Email")
    bio = models.TextField(blank=True, null=True, verbose_name="Биография")
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    is_email_verified = models.BooleanField(
        default=False, verbose_name="Email подтвержден")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
    )

    def followers_count(self):
        """Количество подписчиков"""
        return self.followers.count()

    def following_count(self):
        """Количество подписок"""
        return self.following.count()

    def get_full_name(self):
        """Возвращает полное имя как 'Имя Фамилия'"""
        return f"{self.first_name} {self.last_name}".strip()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписки на пользователей."""
    follower = models.ForeignKey(
        CustomUser,
        related_name="following",
        on_delete=models.CASCADE,
        verbose_name="Подписчик"
    )
    following = models.ForeignKey(
        CustomUser,
        related_name="followers",
        on_delete=models.CASCADE,
        verbose_name="На кого подписан"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата подписки")

    class Meta:
        unique_together = ("follower", "following")
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.follower} подписан на  {self.following}"
