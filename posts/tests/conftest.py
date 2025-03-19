import pytest
import django
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()


@pytest.fixture(scope="session", autouse=True)
def django_setup():
    """Настройка Django перед запуском тестов (один раз за сессию)."""
    django.setup()


@pytest.fixture
def test_user(db):
    """Фикстура для создания тестового пользователя."""
    return User.objects.create_user(username="testuser", email="test@example.com", password="password123")


@pytest.fixture
def another_user(db):
    """Фикстура для создания второго пользователя."""
    return User.objects.create_user(username="anotheruser", email="another@example.com", password="password456")


@pytest.fixture
def test_post(db, test_user):
    """Фикстура для создания тестового поста"""
    return Post.objects.create(user=test_user, content="Test Post")
