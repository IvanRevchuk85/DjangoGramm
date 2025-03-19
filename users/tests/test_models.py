import pytest
from django.core.exceptions import ValidationError
from users.models import CustomUser, Follow
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
import os


@pytest.mark.django_db
def test_create_user(test_user):
    """Тест создания нового пользователя."""
    assert test_user.username == "testuser"
    assert test_user.email == "test@example.com"
    assert test_user.check_password("password123")
    assert test_user.get_full_name() == "Test User"
    assert test_user.bio == "This is a test bio"
    assert test_user.is_email_verified is True


@pytest.mark.django_db
def test_unique_email():
    """Тест уникальности email пользователей."""
    CustomUser.objects.create_user(
        username="user1", email="unique@example.com", password="pass123")
    with pytest.raises(ValidationError):
        user = CustomUser(username="user2", email="unique@example.com")
        user.full_clean()


@pytest.mark.django_db
def test_user_str(test_user):
    """Тест метода __str__() у модели пользователя."""
    assert str(test_user) == "testuser"


@pytest.mark.django_db
def test_user_avatar_upload(test_user):
    """Тест загрузки аватара пользователя."""
    temp_image = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    temp_image.write(os.urandom(1024))  # Запись случайных байтов
    temp_image.seek(0)

    uploaded_avatar = SimpleUploadedFile(
        temp_image.name, temp_image.read(), content_type="image/jpeg")
    test_user.avatar = uploaded_avatar
    test_user.save()

    assert test_user.avatar.name.startswith("avatars/")

    temp_image.close()
    os.unlink(temp_image.name)


@pytest.mark.django_db
def test_follow_user(test_user, another_user):
    """Тест подписки на пользователя."""
    follow = Follow.objects.create(follower=test_user, following=another_user)
    assert follow.follower == test_user
    assert follow.following == another_user
    assert Follow.objects.count() == 1


@pytest.mark.django_db
def test_follow_unique_constraint(test_user, another_user):
    """Тест на уникальность подписки (нельзя подписаться дважды)."""
    Follow.objects.create(follower=test_user, following=another_user)
    with pytest.raises(ValidationError):
        duplicate_follow = Follow(follower=test_user, following=another_user)
        duplicate_follow.full_clean()


@pytest.mark.django_db
def test_followers_count(test_user, another_user):
    """Тест метода followers_count()"""
    Follow.objects.create(follower=another_user, following=test_user)
    assert test_user.followers_count() == 1
    assert another_user.followers_count() == 0


@pytest.mark.django_db
def test_following_count(test_user, another_user):
    """Тест метода following_count()."""
    Follow.objects.create(follower=test_user, following=another_user)
    assert test_user.following_count() == 1
    assert another_user.following_count() == 0
